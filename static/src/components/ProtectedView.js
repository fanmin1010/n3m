import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as actionCreators from '../actions/data';

function mapStateToProps(state) {
  return {
    data: state.data,
    token: state.auth.token,
    loaded: state.data.loaded,
    isFetching: state.data.isFetching,
  };
}


function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
export default class ProtectedView extends React.Component {
  componentDidMount() {
    this.fetchData();
  }


  fetchData() {
    const token = this.props.token;
    this.props.fetchProtectedData(token);
  }

  render() {
    return (
            <div>
                {!this.props.loaded
                    ? <h1>Loading data...</h1>
                    :
                    <div>
                        <h1>Welcome back,</h1>
                        <h1>Are you ready to party?</h1>
                    </div>
                }
            </div>
        );
  }
}

ProtectedView.propTypes = {
  fetchProtectedData: React.PropTypes.func,
  loaded: React.PropTypes.bool,
  userName: React.PropTypes.string,
  data: React.PropTypes.any,
  token: React.PropTypes.string,
};
