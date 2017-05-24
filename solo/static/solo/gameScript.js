
const logoImage = (<img src="static/solo/Logo.svg"/>);
const undoButton = (<button className="menuStyle" onClick = {Undo}>UNDO</button>);

var mapSizeX;
var mapSizeY; 

var mapArray;

var inited = 0;
	
	
function SetupGame(){
	
	$.ajax({
		url: "/setupGame",
		context: document.body	
	}).done(function(data) {
		mapSizeX = data[0]
		mapSizeY = data[1]
		
	})
	
	inited = 1;
}

function LeftClick(x, y){
	$.ajax({
		url: "/leftClick?x="+x+"&y="+y,
		type: 'get'
	})
	
}

function RightClick(x, y){
	$.ajax({
		url: "/rightClick?x="+x+"&y="+y,
		type: 'get'
	})
	
}

function Undo(){
		$.ajax({
		url: "/undo"
	})
}

function RenderMap(){
	
	$.ajax({
		url: "/updateMap",
		context: document.body	
	}).done(function(data) {
		console.log(data)
		mapArray = data
		
	})
	
	if (!mapArray || !mapArray[0]) {
			return <div>Loading</div>;
		}
		var output = [];
	
		for(var cnt1 = 0; cnt1 < mapSizeY; cnt1++){
			output.push([]);
			for(var cnt2 = 0; cnt2 < mapSizeX; cnt2++){
				let outX = cnt2, outY = cnt1;
				if(mapArray[cnt1][cnt2] == null){
					output[cnt1].push(<td><button className="tileButton" onClick = {() => LeftClick(outX,outY)} onContextMenu = {() => RightClick(outX,outY)}>0</button></td>);
				}else if(mapArray[cnt1][cnt2] == -1)
					output[cnt1].push(<td><button className="tileButtonFlag" onContextMenu = {() => RightClick(outX,outY)}> F </button></td>);
				else if(mapArray[cnt1][cnt2] == 0)
					output[cnt1].push(<td><button className="tileButton0" disabled> {mapArray[cnt1][cnt2]} </button></td>);
				else if(mapArray[cnt1][cnt2] == 9)
					output[cnt1].push(<td><button className="tileButtonMine" disabled> M </button></td>);
				else
					output[cnt1].push(<td><button className={"tileButton"+ mapArray[cnt1][cnt2]} disabled> {mapArray[cnt1][cnt2]} </button></td>);
			}
			output[cnt1] = <tr className="mapGrid">{output[cnt1]}</tr>;
		}
	
	return <tables>{output}</tables>
}


function main(){
	
	if(!inited)
		SetupGame();
	
	ReactDOM.render(
		<div>
		<RenderMap />
		<br />
		{undoButton}
		</div>,
		document.getElementById('root')
	);
}

setInterval(main,100);





















