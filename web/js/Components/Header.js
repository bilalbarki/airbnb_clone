import React from 'react';

/*defines the header*/

class Header extends React.Component {
   render() {
	   	
	     var divStyle = {
	     	width:200,
	     	background:'#ffffff',
	     }
	     return (
	         <header className="header">
	           <img src="./static/logo.png" className="logo" />
	           <div style={divStyle}></div>
	         </header>
	      );
   	}
}

export default Header;
