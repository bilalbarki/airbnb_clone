import { STATE_FETCH_INITIATED, STATE_FETCH_COMPLETED, STATE_FETCH_ERROR } from '../Constants/StateConstants.js';

/*reducer for states*/
function statesReducer(state = {}, action) {
	switch (action.type) {
		case STATE_FETCH_INITIATED:
      		return Object.assign({}, state, {
        		isFetching: true,
        		didInvalidate: false,
      		})
      	case STATE_FETCH_COMPLETED:
      		return Object.assign({}, state, {
		        isFetching: false,
		        entities: action.entities,
		        didInvalidate: false,
		        receivedAt: Date.now()
		     })

		default:
      		return state
      	}
}

export default statesReducer;