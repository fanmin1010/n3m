# Application Modifications.

### Basic View Example.
cd statics/src/
modify routes.js by adding an import line for a new page.
e.g. add the following toward the top of routes.js
```
import Profile from '.components/Profile';
```
Then in the default Route Path add a route. e.g.
```
<Route path="profile" component={requireAuthentication(ProfileView)} />
```
Notice that here I have chosen to require authentication. Take a look at the Authentication components to see more about how this works.

Now lets create a basic view ./components/ProfileView.js. From the most basic perspective all that is needed to import is the following: 
```
import React from 'react';
```
but seeing as we are using material-ui, you also want to import some components:
```
import Avatar from 'material-ui/Avatar';
```
and because we will need to read data we want to use our redux components:
```
import { bindActionCreators } from 'redux';  
import { connect } from 'react-redux'; 
```

Because this view will only be displaying data, we use a function that pulls data from the global state object provided by redux and maps is to properties used locally:
```
 function mapStateToProps(state) {
    return {
      data: state.data,
      loaded: state.data.loaded
    };
  }
```
We also map events that modify properties back to the state:
```
function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}
```
Then connect both back to the present view
```
@connect(mapStateToProps, mapDispatchToProps)
```
and  the begin to actually create the view:
```
export default class ProfileView extends React.Component {
  render() {
    return ({ DOM STUFF GOES HERE });
  }
}
```
Finally, we need a way to get to this view. So we add a link into the header menu. src/components/Header/index.js:
```
  <MenuItem onClick={() => this.dispatchNewRoute('/profile')}>
    Profile
  </MenuItem>
```
That's it!

