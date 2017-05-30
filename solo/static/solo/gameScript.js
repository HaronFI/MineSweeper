

//Render Map class
class RenderMap extends React.Component {

	
	constructor(props){
		super(props);
		this.state = {
			mapArray: null,
			mapSizeY: 16,
			mapSizeX: 16,
			gameState: 0,
			gameID: 1,
		};
		
		this.UpdateMap = this.UpdateMap.bind(this);
		this.LeftClick = this.LeftClick.bind(this);
		this.RightClick = this.RightClick.bind(this);
		this.Undo = this.Undo.bind(this);
		this.getGameState = this.getGameState.bind(this);
		this.resetGame = this.resetGame.bind(this);
	}
	
	componentDidMount(){
		self = this;
		
		$.ajax({
			url: "/getSize",
			context: document.body	
		}).done(function(data) {
			console.log(data)
			self.setState({mapSizeX : data[0]})
			self.setState({mapSizeY : data[1]})
			
			self.UpdateMap()
			
		});
		
		//setInterval(self.UpdateMap, 1000);
	}

	

	UpdateMap(){
		$.ajax({
			url: "/getMap",
			context: document.body	
		}).done(function(data) {
			console.log(data)
			self.setState({mapArray: data})
			self.getGameState()
		})
		
	}
	
	
	LeftClick(x, y){
		$.ajax({
			url: "/leftClick?x="+x+"&y="+y,
			type: 'get'
		}).done(function(data) {
				console.log(data)
				self.setState({mapArray: data})
				self.getGameState()
			})
		
	}
	
	
	RightClick(x, y){
		$.ajax({
			url: "/rightClick?x="+x+"&y="+y,
			type: 'get'
		}).done(function(data) {
				console.log(data)
				self.setState({mapArray: data})
				self.getGameState()
			})
		
	}

	Undo(){
		$.ajax({
			url: "/undo"
		}).done(function(data) {
				console.log(data)
				self.setState({mapArray: data})
				self.getGameState()
			})
	}
	
	getGameState(){
		$.ajax({
			url: "/getGameState"
		}).done(function(data) {
				console.log(data)
				self.setState({gameState: data})
			})
	}
	
	resetGame(){
		window.location.href = "/";
	}
	
	render(){
	
	
	const undoButton = (<button className="menuStyle" onClick = {this.Undo}>UNDO</button>);
	const resetButton = (<button className="menuStyle" onClick = {this.resetGame}>RESET</button>);
		
	if (!this.state.mapArray || !this.state.mapArray[0]) {
		return <div>Loading</div>;
	}
	var output;
	
	if(self.state.gameState == 0){
		output = []
		for(var cnt1 = 0; cnt1 < this.state.mapSizeY; cnt1++){
			output.push([]);
			for(var cnt2 = 0; cnt2 < this.state.mapSizeX; cnt2++){
				let outX = cnt2, outY = cnt1;
				if(this.state.mapArray[cnt1][cnt2] == null){
					output[cnt1].push(<td key = {cnt1+","+cnt2}><button className="tileButton" onClick = {() => this.LeftClick(outX,outY)} onContextMenu = {(event) => {event.preventDefault(); this.RightClick(outX,outY)}}>0</button></td>);
				}else if(this.state.mapArray[cnt1][cnt2] == -1)
					output[cnt1].push(<td key = {cnt1+","+cnt2}><button className="tileButtonFlag" onContextMenu = {(event) => {event.preventDefault(); this.RightClick(outX,outY)}}> F </button></td>);
				else if(this.state.mapArray[cnt1][cnt2] == 0)
					output[cnt1].push(<td key = {cnt1+","+cnt2}><button className="tileButton0" disabled> {this.state.mapArray[cnt1][cnt2]} </button></td>);
				else if(this.state.mapArray[cnt1][cnt2] == 9)
					output[cnt1].push(<td key = {cnt1+","+cnt2}><button className="tileButtonMine" disabled> M </button></td>);
				else
					output[cnt1].push(<td key = {cnt1+","+cnt2}><button className={"tileButton"+ this.state.mapArray[cnt1][cnt2]} disabled> {this.state.mapArray[cnt1][cnt2]} </button></td>);
			}
			output[cnt1] = <tr key = {cnt1} className="mapGrid">{output[cnt1]}</tr>;
		}
	}else if(self.state.gameState == 2){
		output = <div><br /><img src="/static/solo/Lose.svg"/></div>
	}else if(self.state.gameState == 3){
		output = <div><br /><img src="/static/solo/Win.svg"/></div>
	}
		return <div>{resetButton}{undoButton}<br /><tables className="centerDiv">{output}</tables></div>
	}
	
}


ReactDOM.render(
	<div>
	<RenderMap />
	</div>,
	document.getElementById('root')
);





















