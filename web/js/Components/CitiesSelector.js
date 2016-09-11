import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import { CITY_FETCH_INITIATED, CITY_FETCH_COMPLETED, CITY_FETCH_ERROR, CITY_SELECTED, NO_STATE_SELECTED } from '../Constants/CityConstants.js';
import {selectCity} from '../Actions/CityActionCreators';
import CityItemSelector from './CityItemSelector';

/*Cities Selector Component*/
class CitiesSelector extends React.Component {
	createListItems() {
		return Object.keys(this.props.state_cities.entities[this.props.state_id]['cities']).map((key) => {
   			return (
   				<CityItemSelector city_id={key} key={key} state_id={this.props.state_id}>
   					{this.props.state_cities.entities[this.props.state_id]['cities'][key]['name']}
   				</CityItemSelector>
   				);
    
		});
	}

	shouldComponentUpdate(nextProps, nextState) {
  		return (nextProps.state_cities['fetch_state_id'] === this.props.state_id);
	}

	citiesList() {
		if (this.props.state_cities['isFetching'] && this.props.state_cities['fetch_state_id'] === this.props.state_id) {
   			return (<h2>is fetching...</h2>);
   		}
   		else if(Object.keys(this.props.state_cities.entities[this.props.state_id]['cities']).length === 0) {
   			return (<div>empty</div>)
   		}
   		else {
   			return (this.createListItems());
   		}
	}

	render() {
		
	     return (
	     	<div className="citiesContainer">
		         <ul className="citiesList">
		           {this.citiesList()}
		         </ul>
	        </div>
	      );
   	}
}

function mapStateToProps(state) {
	return {
		state_cities: state.cities
	};
}

function matchDispatchToProps(dispatch) {
	return bindActionCreators({
		selectCity
	}, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(CitiesSelector);
