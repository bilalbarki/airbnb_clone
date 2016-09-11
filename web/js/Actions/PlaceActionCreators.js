import { PLACE_FETCH_INITIATED, PLACE_FETCH_COMPLETED, PLACE_FETCH_ERROR, PLACE_SELECTED, PLACE_FETCH_EMPTY } from '../Constants/PlaceConstants.js';
import { normalize, Schema, arrayOf } from 'normalizr';
import request from 'superagent';
import { API_URL } from '../../config';

/*initiate place fetch*/
export function placeFetchInitiate() { 	
  return {
    type: PLACE_FETCH_INITIATED,
  }
}

/*signal place fetch is complete*/
export function placeFetchCompleted(json) {
	return {
		type: PLACE_FETCH_COMPLETED,
		entities: json
	}
}

/*req function from api*/
function reqStates(url, callback, result = []) {
	
	request.get(url).set('Access-Control-Allow-Credentials', 'true')
		.then( (response) => 
		{
			console.log('asdas');
			for (let i=0; i<response.body.data.length; i++)
				result.push(  response.body.data[i] );
			
			if (response.body.paging.next) {

				reqStates(response.body.paging.next, callback, result);
			}
			else {

				callback(result);
			}
		}, (error) => {
			console.error("Failed!", error);
		});
}

/*gets all places by state*/
function getAllPlacesByState(states, result, callback) {
	
	var items_processed = 0;
	if (states.length !== 0) {
			states.map( (state_id) => { 

				reqStates(`${API_URL}/states/${state_id}/places`, (json) => {
					items_processed++;
					const places = new Schema('places');
					let norm_json = normalize(json, arrayOf(places));
					console.log("ta", norm_json.entities);
					Object.assign(result.places, norm_json.entities.places);
					if (items_processed === states.length) {
						callback();
					}
					
				});
			});
			
		}
		else {
			callback();
		}
}

/*gets all places by state and city*/
function getAllPlacesByStateAndCity(cities, result, callback) {
	var items_processed = 0;
	if (cities.length !== 0) {
			cities.map( (data) => { 

				reqStates(`${API_URL}/states/${data.state_id}/cities/${data.city_id}/places`, (json) => {
					items_processed++;
					const places = new Schema('places');
					let norm_json = normalize(json, arrayOf(places));
					console.log("ta", norm_json.entities);
					Object.assign(result.places, norm_json.entities.places);
					if (items_processed === cities.length) {
						callback();
					}
					
				});
			});
			
		}
		else {
			callback();
		}
}

/*dispatches the state fetch complete function*/
function dispatchFetchComplete(check, dispatch, resultByState, resultByCity) {
	if (check == 2) {
		Object.assign(resultByState.places, resultByCity.places);
		dispatch( placeFetchCompleted(resultByState) );
	}
}

/*fetch places*/
export function fetchPlaces(filter) {
	console.log(filter);
	return function(dispatch) {
		dispatch( placeFetchInitiate() );
		
		if (filter.states.length !=0 || filter.cities.length != 0) {
			let resultByState = {places:{},};
			let resultByCity = {places:{},};
			let check = 0;
			getAllPlacesByState(filter.states, resultByState, () => {
				check++;
				dispatchFetchComplete(check, dispatch, resultByState, resultByCity);
			});
			getAllPlacesByStateAndCity(filter.cities, resultByCity, () => {
				check++;
				dispatchFetchComplete(check, dispatch, resultByState, resultByCity);
			});
		}
		else {
			reqStates(`${API_URL}/places`, (json) => {
				const places = new Schema('places');
				let norm_json = normalize(json, arrayOf(places));
		
				dispatch( placeFetchCompleted(norm_json.entities) );		
			});
		}
		
	}
}

/*place selection*/
export function selectPlace(state, checked) {
	console.log("You clicked on ", state.name);
	return {
		type: STATE_SELECTED,
		state_id: state.id,
		checked: checked
	}
}
