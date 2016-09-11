import { STATE_FETCH_INITIATED, STATE_FETCH_COMPLETED, STATE_FETCH_ERROR, STATE_SELECTED, STATE_FETCH_EMPTY } from '../Constants/StateConstants.js';
import { normalize, Schema, arrayOf } from 'normalizr';
import request from 'superagent';
import { API_URL } from '../../config';

/*initiate states fetch*/
export function stateFetchInitiate() { 	
  return {
    type: STATE_FETCH_INITIATED,
  }
}

/*runs after state fetch is complete*/
export function stateFetchCompleted(json) {
	return {
		type: STATE_FETCH_COMPLETED,
		entities: json
	}
}

/*req function, takes care of pagination*/
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

/*fetch States*/
export function fetchStates() {
	return function(dispatch) {
		dispatch( stateFetchInitiate() );

		/*request.get('http://localhost:3333/users')
			.then( (response) => {
		  		let json = normalize(response.body.data, arrayofstates);
		  		dispatch( stateFetchCompleted(json['entities']['states']) )
			}, (error) => {
		  		console.error("Failed!", error);
		});*/
		reqStates(`${API_URL}/states`, (json) => {
				const state = new Schema('states');
				let norm_json = normalize(json, arrayOf(state));
				console.log("this", norm_json);
				dispatch( stateFetchCompleted(norm_json.entities) );	
				

		});
	}
}

/*runs when a state is selected or unselected*/
export function selectState(state, checked) {
	console.log("You clicked on ", state.name, checked);
	return {
		type: STATE_SELECTED,
		state_id: state.id,
		checked: checked
	}
}
