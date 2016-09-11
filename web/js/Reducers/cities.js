import { CITY_FETCH_INITIATED, CITY_FETCH_COMPLETED, CITY_FETCH_ERROR, CITY_SELECTED, NO_STATE_SELECTED } from '../Constants/CityConstants.js';
import { STATE_FETCH_INITIATED, STATE_FETCH_COMPLETED, STATE_FETCH_ERROR, STATE_SELECTED } from '../Constants/StateConstants.js';

const initialCitiesState = {
	entities: {},
	isFetching: null,
	fetch_state_id: null
} 

/*reducer for cities*/
function citiesReducer(state = initialCitiesState, action) {
	switch (action.type) {
		case CITY_FETCH_INITIATED:
      		return Object.assign({}, state, {
        		isFetching: true,
        		fetch_state_id: action.fetch_state_id
      		});
      	case CITY_FETCH_COMPLETED:

      		let test = Object.assign({}, state, {
        		isFetching: false,
        		
      		});
      		Object.assign(test.entities, action.entities);
      		
      		return test;

		default:
      		return state
      	}
}

export default citiesReducer;