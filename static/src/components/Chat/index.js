import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';
import Paper from 'material-ui/Paper';
import { bindActionCreators } from 'redux';

import * as actionCreators from '../../actions/auth';

function mapStateToProps(state) {
  return {
    token: state.auth.token,
    userName: state.auth.userName,
    isAuthenticated: state.auth.isAuthenticated
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}


const style = {
  height: '100%',
  width: '50%',
  margin: '0 auto',
  textAlign: 'center',
  display: 'inline-block',
};
  

@connect(mapStateToProps, mapDispatchToProps)
export class Chat extends Component {
  constructor(props) {
    super(props);
    this.state = {
      party: {name: 'Clark Kent'}
    };

  }

  render() {
    return (
						<div>
							<Paper style={style} zDepth={5} rounded={false} />
						</div>
        );
  }
}

Chat.propTypes = {
  logoutAndRedirect: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool,
};

