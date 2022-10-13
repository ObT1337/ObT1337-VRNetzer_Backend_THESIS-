
var container, stats, controls;
var camera, scene, renderer;

var raycaster, mouse;

init();
render();


function RGB2HTML(red, green, blue)
{
  var decColor =0x1000000+ blue + 0x100 * green + 0x10000 *red ;
  return '#'+decColor.toString(16).substr(1);
}

function init() {

  container = document.createElement('div');
  document.body.appendChild(container);

  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.25, 20);
  camera.position.set(-1.8, 0.9, 2.7);

  scene = new THREE.Scene();

  raycaster = new THREE.Raycaster();
  mouse = new THREE.Vector2()


 const ngeometry = new THREE.BoxGeometry( 1,1,1);
 const nmaterial = new THREE.MeshBasicMaterial( { color:RGB2HTML(255,255,0)} );//"rgb(155, 102, 102)" 
const cube = new THREE.Mesh( ngeometry, nmaterial );
                //console.log(data['nodes'][i]["p"]);
scene.add( cube );
                //cube.position.set(0, 10, 0);
cube.position.set(10,0,0); //0x00ff00


  renderer = new THREE.WebGLRenderer({
    antialias: true
  });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  renderer.outputEncoding = THREE.sRGBEncoding;
  container.appendChild(renderer.domElement);

  var pmremGenerator = new THREE.PMREMGenerator(renderer);
  pmremGenerator.compileEquirectangularShader();

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.addEventListener('change', render); // use if there is no animation loop
  controls.minDistance = 2;
  controls.maxDistance = 10;
  controls.target.set(0, 0, -0.2);
  controls.update();

  window.addEventListener('resize', onWindowResize, false);

  renderer.domElement.addEventListener('click', onClick, false);

}

function onClick() {

  event.preventDefault();

  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);

  var intersects = raycaster.intersectObject(scene, true);

  if (intersects.length > 0) {
	
		var object = intersects[0].object;

    object.material.color.set( Math.random() * 0xffffff );

  }
	
	render();

}

function onWindowResize() {

  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(window.innerWidth, window.innerHeight);
  
  render();

}


function render() {

  renderer.render(scene, camera);

}
