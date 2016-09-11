import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import Places from './Places';

/*this is the content which displays filtered places*/
class Content extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
  
      };
    }

   render() {
	     return (
  	     <div className="Content">
            <Places />
         </div>
	      );
   	}
}

function mapStateToProps(state) {
  return {
    
  };
}

function matchDispatchToProps(dispatch) {
	return bindActionCreators({
		
	}, dispatch);
}
export default connect(mapStateToProps, matchDispatchToProps)(Content);
