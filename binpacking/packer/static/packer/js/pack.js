function draw(data, scene, material) {
	$.each(data, function(i, box)
	{
		var geometry = new THREE.BoxGeometry(box.w, box.h, box.d);
		var cube = new THREE.Mesh(geometry, material);
		cube.position.set(0, 0, 0);
		scene.add(cube);
	});
}

$( document ).ready(function(){
	var scene = new THREE.Scene();
	var screen = $("#screen");
	var width = screen.width();
	var height = screen.height();
	var ratio = width / height;
	
	var camera = new THREE.PerspectiveCamera( 100, ratio, 0.1, 1000 );
	camera.position.x = 3;
	camera.position.y = 2;
	camera.position.z = 5;
	
	var renderer = new THREE.WebGLRenderer();
	renderer.setSize(width, height);
	
	var material = new THREE.MeshNormalMaterial({transparent: true, opacity: 0.75});//, wireframe: true});
	
	$('#add').click(function(){
		var boxRaw = $($('#boxRaw')[0]).clone();
		boxRaw.removeAttr('id');
		$('#boxContainer').append(boxRaw);
	});
	
	$('#start').click(function(){
	
		var inputs = $('#binRaw').find('input');
		var bin = {
			w: $(inputs[0]).val(),
			h: $(inputs[1]).val(),
			d: $(inputs[2]).val(),
			n: $(inputs[3]).val()};
		
		var boxes = [];
		$('#boxContainer .boxRaw').each(function(i, item){
			var inputs = $(item).find('input');
			boxes.push({
				w: $(inputs[0]).val(),
				h: $(inputs[1]).val(),
				d: $(inputs[2]).val(),
				n: $(inputs[3]).val()
			});
		});
		
		$.get('/pack/', {bin: JSON.stringify(bin), boxes: JSON.stringify(boxes)})
	      .done(function (data) {
	    	  screen.empty();
	    	  screen.append(renderer.domElement);
	    	  
	    	  controls = new THREE.OrbitControls( camera, renderer.domElement );
	    	  
	    	  draw(data, scene, material);
	    	  
    		var render = function () {
    			requestAnimationFrame( render );
    			renderer.render(scene, camera); };
    		render();
	      });
	    
		console.log(boxes);
	});
});