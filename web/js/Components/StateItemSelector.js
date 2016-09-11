import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {selectState} from '../Actions/StateActionCreators';
import { STATE_FETCH_INITIATED, STATE_FETCH_COMPLETED, STATE_FETCH_ERROR, STATE_SELECTED } from '../Constants/StateConstants.js';
import CitiesSelector from './CitiesSelector';
import {fetchCities} from '../Actions/CityActionCreators';

/*All State Items are listed by this, provide state_id as props*/
class StateItemSelector extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
          expand: false,
      };
    }

  toggle_expand() {
    if (this.state.expand == false) {
        if (this.refs.stateCheckbox.checked) {
            this.refs.stateCheckbox.checked=!this.refs.stateCheckbox.checked;
            this.props.selectState(this.props.state_states.entities['states'][this.props.state_id], this.refs.stateCheckbox.checked);
        }
    }
    this.setState({
      expand: !this.state.expand
    });
    
  }

  show_cities(key) {
    this.props.fetchCities(key);
    this.toggle_expand();
  }

  arrowhead() {
    if (this.state.expand) {
      return "\u25B2";
    }
    else {
      return "\u25BC";
    }
  }

  

   render() {
        var selectedStateStyle = {
          background: '#666666',
          color: '#ffffff',
        };
	     return (
  	    <li className="stateItems"> 	
            <div className="fetchedStates">
                
                    <input 
                        type="checkbox" className="checkbox"
                       
                        ref="stateCheckbox" onChange={(e) => {this.props.selectState(this.props.state_states.entities['states'][this.props.state_id], e.target.checked)}}
                    />
                    <div className="stateText" onClick={() => {this.refs.stateCheckbox.checked=!this.refs.stateCheckbox.checked; 
                        this.props.selectState(this.props.state_states.entities['states'][this.props.state_id], this.refs.stateCheckbox.checked);
                    }}>
                        {this.props.children}
                    </div>
               
            
                <div className="arrowHead" key={this.props.state_id} onClick={(e) => this.show_cities(this.props.state_id)}>
                    {this.arrowhead()}
                </div>
            </div>
            {(() => {
                if (this.state.expand) {
                    return (<CitiesSelector state_id={this.props.state_id}/>);
                }
            })()}
        </li>
	   );
   	}
}

function mapStateToProps(state) {
  return {
    state_states: state.states,
    state_cities: state.cities,
  };
}

function matchDispatchToProps(dispatch) {
	return bindActionCreators({
		selectState,
    fetchCities,
	}, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(StateItemSelector);
