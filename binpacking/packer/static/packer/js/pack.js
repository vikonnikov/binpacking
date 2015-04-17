function draw(box, scene, material)
{
    var geometry = new THREE.BoxGeometry(box.w, box.h, box.d);
    var cube = new THREE.Mesh(geometry, material);
    var x = parseFloat(box.x) + parseFloat(box.w) / 2;
    var y = parseFloat(box.y) + parseFloat(box.h) / 2;
    var z = parseFloat(box.z) + parseFloat(box.d) / 2;

    var edge = new THREE.EdgesHelper( cube, 0x00ffff );
    cube.position.set(x, y, z);
    scene.add(cube);
    scene.add(edge);
}

function buildAxes( length ) {
    var axes = new THREE.Object3D();

    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( length, 0, 0 ), 0xFF0000, false ) ); // +X
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( -length, 0, 0 ), 0xFF0000, true) ); // -X
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, length, 0 ), 0x00FF00, false ) ); // +Y
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, -length, 0 ), 0x00FF00, true ) ); // -Y
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, 0, length ), 0x0000FF, false ) ); // +Z
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, 0, -length ), 0x0000FF, true ) ); // -Z

    return axes;

}

function clear(scene) {
    $.each(scene.children.slice(1), function(i, item) {
        scene.remove(item);
    });
}

function buildAxis( src, dst, colorHex, dashed ) {
    var geom = new THREE.Geometry(),
        mat;

    if(dashed) {
        mat = new THREE.LineDashedMaterial({ linewidth: 3, color: colorHex, dashSize: 3, gapSize: 3 });
    } else {
        mat = new THREE.LineBasicMaterial({ linewidth: 3, color: colorHex });
    }

    geom.vertices.push( src.clone() );
    geom.vertices.push( dst.clone() );
    geom.computeLineDistances(); // This one is SUPER important, otherwise dashed lines will appear as simple plain lines

    var axis = new THREE.Line( geom, mat, THREE.LinePieces );

    return axis;

}

$( document ).ready(function(){
	var scene = new THREE.Scene();
	var screen = $("#screen");
	var width = screen.width();
	var height = screen.height();
	var ratio = width / height;
	
	var camera = new THREE.PerspectiveCamera( 100, ratio, 0.1, 1000 );
	camera.position.x = 5;
	camera.position.y = 5;
	camera.position.z = 10;
	
	var renderer = new THREE.WebGLRenderer();
	renderer.setSize(width, height);

    var controls = new THREE.OrbitControls( camera, renderer.domElement, screen[0] );
	
	var bin_material = new THREE.MeshNormalMaterial({transparent: true, opacity: 0.25});
    var box_material = new THREE.MeshNormalMaterial({transparent: true, opacity: 0.75});

    screen.append(renderer.domElement);

    var axes = buildAxes( 1000 );
    scene.add( axes );

	$('#add').click(function(){
		var boxRaw = $($('#boxRaw')[0]).clone();
		boxRaw.removeAttr('id');
		$('#boxContainer').append(boxRaw);
	});

	$('#delete').click(function(){
        var items = $('#boxContainer .boxRaw');
        if ( items.length > 1)
		    $($('#boxContainer .boxRaw').get(-1)).remove();
	});

    $('#clear').click(function() {
        clear(scene);
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
		
		var algorithm = $('input[name="algorithm"]:checked').val().toLowerCase();
		
		$.get('/pack/', {algorithm: algorithm, bin: JSON.stringify(bin), boxes: JSON.stringify(boxes)})
	      .done(function (data) {
              clear(scene);

              bin.x = bin.y = bin.z = 0;
              draw(bin, scene, bin_material);

              $.each(data, function(i, box) {
                  draw(box, scene, box_material);
              });

    		var render = function () {
    			requestAnimationFrame( render );
    			renderer.render(scene, camera); };
    		render();
	      });
	    
		console.log(boxes);
	});
});