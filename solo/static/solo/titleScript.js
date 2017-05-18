

function main() {
	
	const logoImage = (<img src="static/solo/logo.svg"></img>);
	
	const soloModeButton = (<button>SOLO MODE</button>);
	
	const centerBox = (<div>
						{logoImage}
						<br/>
						<br/>
						</div>);
	
	
	ReactDOM.render(
		centerBox,
		document.getElementById('root')
	);
}

setInterval(main, 1000);