import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware } from 'redux';
import {Provider} from 'react-redux';
import thunkMiddleware from 'redux-thunk';


import allReducers from './Reducers/all_reducers';
import App from './Components/all_components';
import {fetchStates} from './Actions/StateActionCreators';
import {fetchPlaces} from './Actions/PlaceActionCreators';

const store = createStore(
   allReducers,
   applyMiddleware(
     thunkMiddleware, // lets us dispatch() functions
   )
)

/*initially we want all States and Places data*/
store.dispatch( fetchStates());
store.dispatch( fetchPlaces({    
    	states : [], 
    	cities : [],
}) );

ReactDOM.render(
	(
		<Provider store={store}>
   			<App />
    	</Provider>   
	),
	document.getElementById('app')
);