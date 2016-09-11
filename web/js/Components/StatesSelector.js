import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import { STATE_FETCH_INITIATED, STATE_FETCH_COMPLETED, STATE_FETCH_ERROR, STATE_SELECTED } from '../Constants/StateConstants.js';
import StateItemSelector from './StateItemSelector'; 

/*main states Component*/
class StatesSelector extends React.Component {
	/*creates list items*/
   	createListItems() {

   		return Object.keys(this.props.state_states.entities['states']).map((key) => {
   			
   			return (
   				
   					<StateItemSelector state_id={key} key={key}>
   						{this.props.state_states.entities['states'][key]['name']}
   					</StateItemSelector>
   				);
    
		});
   		
   }

   statesList() {
   	if (this.props.state_states['isFetching']) {
   		return (<h2>is fetching...</h2>);
   	}
   	
   	else if(Object.keys(this.props.state_states.entities).length === 0) {
   		return (<div>empty</div>)
   	}
   	else {
   		return (<ul>{this.createListItems()}</ul>);
   	}
   }

   render() {
	     return (
	     	<div className="states">
	     		<h2 className="statesText">States</h2>
		         <ul className="statesList">
		           {this.statesList()}
		         </ul>
	        </div>
	      );
   	}
}

function mapStateToProps(state) {
	return {
		state_states: state.states
	};
}

function matchDispatchToProps(dispatch) {
	return bindActionCreators({
		
	}, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(StatesSelector);
