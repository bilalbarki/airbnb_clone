import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import PlaceItem from './PlaceItem';

/*main places component*/
class Places extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
  
      };
    }

    placeItems() {
      return Object.keys(this.props.state_places.entities.places).map((key) => {
        
        return (
          
            <PlaceItem place_id={key} key={key} />
          );
    
    });


      
    }

    

   render() {
	   console.log("debug", this.props.state_places);   
      if (this.props.state_places.isFetching) {
        return (
          <div>is fetching...</div>
        );
      }
      else if (Object.keys(this.props.state_places.entities).length === 0 || Object.keys(this.props.state_places.entities.places).length === 0 ) {
        return (
          <div>No places found</div>
        );
      }
      else {
        return (
          <ul className="flex-container">{this.placeItems()}</ul>
        );
      }
   	}
}

function mapStateToProps(state) {
  return {
    state_places: state.places
  };
}

function matchDispatchToProps(dispatch) {
	return bindActionCreators({
		
	}, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(Places);
