import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {fetchPlaces} from '../Actions/PlaceActionCreators';

/*search button component*/
class SearchButton extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
  
      };
    }

   render() {
        
	     return (
  	     <a className="searchButton" onClick={() => this.props.fetchPlaces(this.props.state_places.filters)}>Search</a>
	      );
   	}
}

function mapStateToProps(state) {
  return {
    state_places: state.places
  };
}

function matchDispatchToProps(dispatch) {
	return bindActionCreators({
		fetchPlaces,
	}, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(SearchButton);
