import { PLACE_FETCH_INITIATED, PLACE_FETCH_COMPLETED, PLACE_FETCH_ERROR } from '../Constants/PlaceConstants.js';
import { STATE_SELECTED } from '../Constants/StateConstants.js';
import { CITY_SELECTED } from '../Constants/CityConstants.js';

const initialPlacesState = {
    filters : { 
    	states : [], 
    	cities : [],
    },
    entities : {
    	places: {},
    	is_Fetching : false
    },
    
};

/*searches city id in filter.cities*/
function searchCityId(city_id, myArray){
    for (var i=0; i < myArray.length; i++) {

        if (myArray[i].city_id === city_id) {
            return i;
        }
    }
    return -1;
}

/*reducer for places*/
function placesReducer(state = initialPlacesState, action) {
	switch (action.type) {
		case PLACE_FETCH_INITIATED:
      		return Object.assign({}, state, {
        		isFetching: true,
        		didInvalidate: false,
      		})
      	case PLACE_FETCH_COMPLETED:
      		return Object.assign({}, state, {
		        isFetching: false,
		        entities: action.entities,
		        
		     })
      	case STATE_SELECTED:
      		let test = Object.assign({}, state);
      		if (action.checked) {
      			
      			test.filters.states.push(action.state_id);
      		}
      		else {
      			let index = test.filters.states.indexOf(action.state_id);
      			if (index > -1) {
				    test.filters.states.splice(index, 1);
				}
      		}
      		return test;

      	case CITY_SELECTED:
      		let test2 = Object.assign({}, state);
      		if (action.checked) {
      			test2.filters.cities.push({
      				state_id: action.state_id,
      				city_id: action.city_id
      			});
      		}
      		else {
      			let index = searchCityId(action.city_id, test2.filters.cities);
      			if (index > -1) {
				    test2.filters.cities.splice(index, 1);
				}
      		}
      		return test2;

		default:
      		return state
      	}
}

export default placesReducer;