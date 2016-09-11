import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';


/*Renders a place item, provide place_id as prop*/
class PlaceItem extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
  
      };
    }

    shouldComponentUpdate(nextProps, nextState) {
      return (nextProps.state_places.isFetching !== this.props.state_places.isFetching);
  }

   render() {
      
       return (
         <li className="flex-item">
            
              <div className="placeHeading">
                <h2>{this.props.state_places.entities.places[this.props.place_id].name}</h2>
              </div>
              <div className="placeInnerPadding">    
                 
                  <div className="guests">
                    <div></div>
                    <p className="guestsText">{this.props.state_places.entities.places[this.props.place_id].max_guest} guests max</p>
                  </div>
                  <div className="roomsBathrooms">
                   
                    <p><span className="numberRoomsBathrooms">{this.props.state_places.entities.places[this.props.place_id].number_rooms}</span> &nbsp;rooms</p>
                    <p><span className="numberRoomsBathrooms">{this.props.state_places.entities.places[this.props.place_id].number_bathrooms}</span> &nbsp;bathrooms</p>
                  </div>
                  <div className="description">
                    <p>{this.props.state_places.entities.places[this.props.place_id].description}</p>
                  </div>
                  
                </div>
                <div className="selectPlaceButtonContainer">
                  <a className="buttonPlace">&#36;{this.props.state_places.entities.places[this.props.place_id].price_by_night}&#47;night</a>
                </div>
            
         </li>
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
    
  }, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(PlaceItem);
