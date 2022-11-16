import random
import re

import bs4
import flask
from bs4 import BeautifulSoup as bs


def generate_username():
    """
    If no username is provided, generate a random one and return it
    """
    username = flask.request.args.get("usr")
    if username is None:
        username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
    return username


def has_no_empty_params(rule):
    """
    Filters the route to ignore route with empty params.
    """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def get_all_links(app) -> list[list[str, str]]:
    """Extracts all routes from flask app and return a list of tuples of which the first value is the route and the seconds is the name of the corresponding python function."""
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = flask.url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links


def create_dynamic_links(app: flask.app.Flask):
    """
    Construct the navigation bar
    """
    navbar_html_template = "templates/NavBar_template.html"
    home_html_template = "templates/home_template.html"
    navbar_html = "templates/NavBar.html"
    home_html = "templates/home.html"

    # Get all links from flask
    links = get_all_links(app)

    with open(navbar_html_template, "r") as nav_file:
        nav_soup = bs(nav_file, "html.parser")
    with open(home_html_template, "r") as home_file:
        home_soup = bs(home_file, "html.parser")

    categories = ["home", "main", "nodepanel", "upload", "preview"]

    # initialize the dropdown map
    home_dropdown = nav_soup.find("select", {"id": "home_dropdown"})
    main_dropdown = nav_soup.find("select", {"id": "mainpanel_dropdown"})
    nodepanel_dropdown = nav_soup.find("select", {"id": "nodepanel_dropdown"})
    upload_dropdown = nav_soup.find("select", {"id": "uploader_dropdown"})
    preview_dropdown = nav_soup.find("select", {"id": "preview_dropdown"})
    dropdown_map = {
        "home": home_dropdown,
        "main": main_dropdown,
        "nodepanel": nodepanel_dropdown,
        "upload": upload_dropdown,
        "preview": preview_dropdown,
    }

    # initialize the framebox map
    home_framebox = home_soup.find("div", {"id": "home_framebox"})
    main_framebox = home_soup.find("div", {"id": "mainpanel_framebox"})
    nodepanel_framebox = home_soup.find("div", {"id": "nodepanel_frambox"})
    upload_framebox = home_soup.find("div", {"id": "uploader_framebox"})
    preview_framebox = home_soup.find("div", {"id": "preview_framebox"})
    framebox_map = {
        "home": home_framebox,
        "main": main_framebox,
        "nodepanel": nodepanel_framebox,
        "upload": upload_framebox,
        "preview": preview_framebox,
    }

    for link in links:
        # Skip upload files
        if ("upload" and "files") in link[1]:
            continue
        if link[1] in [
            "nodeinfo",
            "get_structure_scale",
            "test44",
            "force",
            "loadAllProjectsR",
        ]:
            continue
        for category in categories:
            if category in link[1]:
                link = (link[0], link[1].replace(".", " / ").replace("_", " "))
                dropdown_map[category] = add_nav_element(
                    nav_soup, dropdown_map[category], link
                )
                framebox_map[category] = add_home_element(
                    home_soup, framebox_map[category], link
                )

    with open(navbar_html, "w") as nav_file:
        nav_file.write(str(nav_soup))
    with open(home_html, "w") as home_file:
        home_file.write(str(home_soup))


def add_nav_element(
    soup: bs4.BeautifulSoup, dropdown: bs4.element.Tag, link: list[str, str]
):
    """
    Add a new element to the navigation bar.
    """
    # Don't add if already exists
    for element in dropdown.find_all("option"):
        if element["value"] == link[0]:
            return dropdown

    new_element = soup.new_tag("option")
    new_element.string = link[1]
    new_element["value"] = link[0]
    dropdown.append(new_element)
    return dropdown


def add_home_element(
    soup: bs4.BeautifulSoup, framebox: bs4.element.Tag, link: list[str, str]
):
    """
    Adds a new link to the corresponding framebox.
    """
    on_click_event = f"followLink('{link[0]}')"
    for element in framebox.find_all("input"):
        if element["onclick"] == on_click_event:
            return framebox
    new_element = soup.new_tag("input")
    new_element["type"] = "submit"
    new_element["onclick"] = on_click_event
    new_element["value"] = link[1]
    new_element["style"] = "margin: 10px;min-width: 48%; max-width: fit-content;"
    framebox.append(new_element)
    return framebox
