import { CITY_FETCH_INITIATED, CITY_FETCH_COMPLETED, CITY_FETCH_ERROR, CITY_SELECTED } from '../Constants/CityConstants.js';
import { normalize, Schema, arrayOf } from 'normalizr';
import request from 'superagent';
import { API_URL } from '../../config';

/*Initiate city fetch*/
export function cityFetchInitiate(state_id) { 	
  return {
    type: CITY_FETCH_INITIATED,
    fetch_state_id: state_id
  }
}

/*runs after city fetch is done*/
export function cityFetchCompleted(json, state_id) {
	
	return {
		type: CITY_FETCH_COMPLETED,
		entities: {[state_id]: json}

	}
}

/*req function*/
function reqStates(url, callback, result = []) {
	request.get(url).set('Access-Control-Allow-Credentials', 'true')
		.then( (response) => 
		{
			for (let i=0; i<response.body.data.length; i++)
				result.push( response.body.data[i] );
			
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

/*fetch Cities*/
export function fetchCities(state_id) {
	return function(dispatch) {
		dispatch( cityFetchInitiate(state_id) );
		reqStates(`${API_URL}/states/${state_id}/cities`, (json) => {
			if (json.length !== 0) {
				const city = new Schema('cities');
				let norm_json = normalize(json, arrayOf(city));
				
				dispatch( cityFetchCompleted(norm_json.entities, state_id) );
			}
			else {
				dispatch( cityFetchCompleted({cities:{}}, state_id) );
			}
		});
	}
}

/*city selection*/
export function selectCity(city, checked) {
	console.log("You clicked on ", city.name, city.state_id);
	return {
		type: CITY_SELECTED,
		city_id: city.id,
		state_id: city.state_id,
		checked: checked
	}
}
