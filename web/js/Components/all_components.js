import React from 'react';
import Header from './Header';
import Footer from './Footer';
import LeftColumn from './LeftColumn';
import Content from './Content';

/*adds all main components, App is added then to app.js*/
const App = props => (
	<div>
    	<Header />	
    	<div className="main">
    		<LeftColumn />
    		<Content />
    	</div>
    	<Footer />
	</div>
);

export default App;