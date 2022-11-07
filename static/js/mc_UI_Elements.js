
//https://stackoverflow.com/questions/50508717/custom-elements-not-setting-getting-attributes



class mcRButton extends HTMLElement {


    constructor() {
    super();
    }

    connectedCallback() {
      let template = document.querySelector('#mcRB-template').content;
      this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));
    
      let name_button = this.shadowRoot.querySelector("#name");
      let x_button = this.shadowRoot.querySelector("#x");
    
      name_button.textContent = this.getAttribute('name');
      name_button.style.background=this.getAttribute('color');//("background",);
      //console.log('create: '+ this.getAttribute('id'));

      name_button.addEventListener('click', () => {
        //console.log('select '+ this.shadowRoot.getAttribute('id'));
        socket.emit('ex', {msg: this.getAttribute('name'), id: this.getAttribute('id'), fn: "rem_butt_clicked"});
      });
    
      x_button.addEventListener('click', () => {

          console.log(name_button.parentElement);
          var parent = this.getRootNode().host;
          if (parent != null){ //is in shadowDom
            
            socket.emit('ex', {id: this.getAttribute('id'), parent: parent.getAttribute('id'), fn: "rem_butt_del_sbox"});
          }else
          {
            socket.emit('ex', {id: this.getAttribute('id'), parent: this.parentElement.getAttribute('id'), fn: "rem_butt_del"});
          }

      });

    }

}

customElements.define('mc-rbutton', mcRButton);


class mcScrollBox extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {
    let template = document.querySelector('#mcScrollBox-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    
    
    let scrollbox = this.shadowRoot.querySelector("#box");
    let label = this.shadowRoot.querySelector("#label");
    label.innerHTML = this.getAttribute('id').toUpperCase();

    var isScroll = false;
    var lastscroll = 0;
    scrollbox.addEventListener('mouseup', () => {
      //console.log(scrollbox.value);
      isScroll = false;
      //socket.emit('ex', {id: this.getAttribute('id'), val: slider.value, fn: "sli"});
    });

    scrollbox.addEventListener('mousedown', () => {
      isScroll = true;
    });

    scrollbox.addEventListener('scroll', () => {
      var out = [$(scrollbox).scrollTop(), $(scrollbox).scrollLeft() ];
      var thisscroll = out[0] + out[1];
      if (isScroll && Math.abs(thisscroll- lastscroll) > 10){
          socket.emit('ex', {msg: out, id: this.getAttribute('id'), fn: "scb"});
          lastscroll = out[0] + out[1];
          console.log(out[0])

      }
    });
   
  }
}

customElements.define('mc-scrollbox', mcScrollBox);





class mcTextBox extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {
    let template = document.querySelector('#mcTextBox-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    let textbox = this.shadowRoot.querySelector("#text");
    let label = this.shadowRoot.querySelector("#label");
    label.innerHTML = this.getAttribute('id').toUpperCase();

    textbox.addEventListener('keyup', () => {
      console.log(textbox.value);
      socket.emit('ex', {id: this.getAttribute('id'), val: textbox.value, fn: "tex"});
    });

    textbox.addEventListener('change', () => {
      console.log(textbox.value);
      //socket.emit('ex', {id: this.getAttribute('id'), val: slider.value, fn: "sli"});
    });

   
  }
}

customElements.define('mc-textbox', mcTextBox);



class mcColorBox extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {
    let template = document.querySelector('#mcColorBox-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    let colorbox = this.shadowRoot.querySelector("#color");

   
  }
}

customElements.define('mc-colorbox', mcColorBox);



class mcSresult extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {


    let template = document.querySelector('#mcSresult-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    let name_button = this.shadowRoot.querySelector("#name");
    let x_button = this.shadowRoot.querySelector("#x");
  
    name_button.textContent = this.getAttribute('name');
    name_button.style.background=this.getAttribute('color');//("background",);
    //console.log('create: '+ this.getAttribute('id'));

    name_button.addEventListener('click', () => {
      //console.log('select '+ this.shadowRoot.getAttribute('id'));
      socket.emit('ex', {msg: this.getAttribute('name'), id: this.getAttribute('id'), fn: "sres_butt_clicked"});
    });
  

   
  }
}

customElements.define('mc-sresult', mcSresult);



function initDropdown (id, data, active){

  $('#'+ id).selectmenu();

  for (let i = 0; i < data.length; i++) {
    $('#'+ id).append(new Option(data[i]));
  }
  $('#'+ id).val(active);
  $('#'+ id).selectmenu("refresh");

  $('#'+ id).on('selectmenuselect', function () {
    var name =  $('#'+ id).find(':selected').text();
    socket.emit('ex', {id: id, opt: name, fn: "sel"});
    ///logger($('#selectMode').val());
  });

}
function initProjectDropdown (id, data, active){

  $('#'+ id).selectmenu();

  for (let i = 0; i < data.length; i++) {
    $('#'+ id).append(new Option(data[i]));
  }
  $('#'+ id).val(active);
  $('#'+ id).selectmenu("refresh");

  $('#'+ id).on('selectmenuselect', function () {
    var name =  $('#'+ id).find(':selected').text();
    socket.emit('ex', {id: "projects", opt: name, fn: "sel"});
    ///logger($('#selectMode').val());
  });

}


function initProjectDropdown (id, data, active){

  $('#'+ id).selectmenu();

  for (let i = 0; i < data.length; i++) {
    $('#'+ id).append(new Option(data[i]));
  }
  $('#'+ id).val(active);
  $('#'+ id).selectmenu("refresh");

  $('#'+ id).on('selectmenuselect', function () {
    var name =  $('#'+ id).find(':selected').text();
    socket.emit('ex', {id: "projects", opt: name, fn: "sel"});
    ///logger($('#selectMode').val());
  });

}


function initSlider (id){

  $('#'+ id).slider({
      animate: true,
      range: "max",
      min: 0,
      max: 255,
      value: 128,
      slide: function (event, ui) {
        socket.emit('ex', {id: id, val: ui.value, fn: "sli"});
      }
  });

}


function initCheckbox (id){
  $('#'+ id, function(){ 
    socket.emit('ex', {id: id, val: $('#'+ id).is(":checked"), fn: "chk"});
  });

}


function initButton (id){
  $('#'+ id).on("click", function(){
    var $this = $(this);
    socket.emit('ex', { id: id, val: $this.val(), fn: "but" });
  });
}


function initToggle (id, texts){
  $('#'+ id).on("click", function(){
    var $this = $(this);
    if($this.val() == texts[1] ){
        $this.val(texts[0]);         
    } else {
        $this.val(texts[1]);
    }
    socket.emit('ex', {id: id, val: $this.val(), fn: "tgl"}); 
  });

}





function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
            result += characters.charAt(Math.floor(Math.random() * 
            charactersLength));
        }
    return result;
}