import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {selectCity} from '../Actions/CityActionCreators';

/*All City Items are listed by this, provide city_id as props*/
class CityItemSelector extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
        checked: false,
      };
    }

    setCheckedState() {
      
      for (let i=0; i< this.props.city_filters.length; i++) {
        if(this.props.city_id == this.props.city_filters[i].city_id) {
          return true;
        }
      }
      return false;
    } 

   render() {
        
	     return (
  	     <li className="cityItem">
            
              <input 
                defaultChecked={this. setCheckedState()}
                type="checkbox" 
                ref="cityCheckbox" 
                onChange={(event)=>{this.props.selectCity(this.props.state_cities.entities[this.props.state_id]['cities'][this.props.city_id], event.target.checked)}}
              />
              <div className="cityText" onClick={() => {this.refs.cityCheckbox.checked=!this.refs.cityCheckbox.checked; 
                        this.props.selectCity(this.props.state_cities.entities[this.props.state_id]['cities'][this.props.city_id], this.refs.cityCheckbox.checked);

                    }}>
                {this.props.children}
                
              </div>
            
          </li>
	      );
   	}
}

function mapStateToProps(state) {
  return {
    state_cities: state.cities,
    city_filters: state.places.filters.cities,
  };
}

function matchDispatchToProps(dispatch) {
	return bindActionCreators({
		selectCity,
	}, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(CityItemSelector);
