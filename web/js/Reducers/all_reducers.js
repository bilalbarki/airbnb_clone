import {combineReducers} from 'redux';
import statesReducer from './states';
import citiesReducer from './cities';
import placesReducer from './places';

/*combines all the reducers*/
const allReducers = combineReducers({
	states: statesReducer,
	cities: citiesReducer,
	places: placesReducer
});

export default allReducers;