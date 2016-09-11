import React from 'react';
import StatesSelector from './StatesSelector';
import SearchButton from './SearchButton'; 

/*defines the left column within main*/
class LeftColumn extends React.Component {
   render() {
	   	var headerStyle = {
	         display:'flex',
	         height: 600,
	      	 background:'grey',
	      	 width:300,
	     }
	     
	     return (
	         <div className="leftColumn">
	           <div className="buttonHolder">
	           	<SearchButton className="searchButton"/>
	           </div>
	           <StatesSelector />
	         </div>
	      );
   	}
}

export default LeftColumn;
