
//styles
var buttonStyle = {
	fontSize: "32",
	backgroundColor: "dodgerblue",
}
	

function TestFunction(prop){
	
	return(<p><a href="bb">{prop.testWord}</a></p>);
}


ReactDOM.render(
	<TestFunction testWord="TEST"/>,
	document.getElementById('root')
);