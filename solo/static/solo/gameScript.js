//static content
const logoImage = (<img src="static/solo/logo.svg"></img>);


//inline styles
const frameStyle = {
	align: 'center',
};

const mapStyle = {
	borderSpacing: '0px',
	backgroundColor: 'white',
	border: '2px solid white',
};

const mapButtonStyle = {
	backgroundColor: 'dodgerBlue',
	width: '41',
	height: '41',
	color: 'white',
};

const mapPieceStyle = {
	backgroundColor: 'lightgrey',
	width: '42',
	height: '42',
	fontSize: '32px',
	textAlign: 'center',
	border: 'none',	
};

const mapPieceStyle1 = {
	backgroundColor: 'lightgrey',
	width: '42',
	height: '42',
	fontSize: '32px',
	textAlign: 'center',
	border: 'none',
	fontWeight: 'bold',
	color: 'blue',	
};

const mapPieceStyle2 = {
	backgroundColor: 'lightgrey',
	width: '42',
	height: '42',
	fontSize: '32px',
	textAlign: 'center',
	border: 'none',
	fontWeight: 'bold',
	color: 'green',	
};

const mapPieceStyle3 = {
	backgroundColor: 'lightgrey',
	width: '42',
	height: '42',
	fontSize: '32px',
	textAlign: 'center',
	border: 'none',
	fontWeight: 'bold',
	color: 'red',	
};

const mapPieceStyle4 = {
	backgroundColor: 'lightgrey',
	width: '42',
	height: '42',
	fontSize: '32px',
	textAlign: 'center',
	border: 'none',
	fontWeight: 'bold',
	color: 'darkblue',	
};


//elements
const pieceEmpty = (<button style={mapPieceStyle} disabled></button>);
const pieceMine = (<button style={mapPieceStyle} disabled>&#10040;</button>); 
const piece1 = (<button style={mapPieceStyle1} disabled>1</button>);
const piece2 = (<button style={mapPieceStyle2} disabled>2</button>);
const piece3 = (<button style={mapPieceStyle3} disabled>3</button>);
const piece4 = (<button style={mapPieceStyle4} disabled>4</button>);


//global varibles


/*state Key
0 - init
1 - game start
*/
var state = 0
/*mapArray Key
0 - empty 
1
2
3
4
5 - mine
6 - flag
*/
var mapArray = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]];
/*mapButtonArray Key
0 - off
1 - on
2 - disable
*/
var mapButtonArray = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]];

//process functions
function InitFunction(){
	
	for(var cnt = 0; cnt < 16; cnt++){
		for(var cnt2 = 0; cnt2 < 16; cnt2++){
			mapButtonArray[cnt][cnt2] = 1;
		}
	}
	
	state = 1;
}


function RemoveButton(x, y){
	mapButtonArray[x][y] = 0;
}


//components
function MapComponent() {
	
	var cols = [];
	var rows = [];
	
	for(var cnt = 0; cnt < 16; cnt++){
		for(var cnt2 = 0; cnt2 < 16; cnt2++){
			if(mapButtonArray[cnt][cnt2] == 1){
				cols[cnt2] = (<td><button style={mapButtonStyle} onclick="RemoveButton({cnt},{cnt2})"></button></td>);
			}
			else if(mapButtonArray[cnt][cnt2] == 0){
				
			}
		}
		
		rows[cnt] = (<tr>{cols[0]}{cols[1]}{cols[2]}{cols[3]}{cols[4]}{cols[5]}{cols[6]}{cols[7]}{cols[8]}{cols[9]}{cols[10]}{cols[11]}{cols[12]}{cols[13]}{cols[14]}{cols[15]}</tr>);
	}
	
return 	<table style={mapStyle}>{rows}</table>;
}


function main(){
	
	if(state == 0){
		InitFunction();
	}

	ReactDOM.render(
		<div style={frameStyle}>
		{logoImage}
		<br/>
		<MapComponent/>
		</div>,
		document.getElementById('root')
	);
}

setInterval(main, 1000);























