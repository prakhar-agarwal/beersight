import React, { PropTypes } from 'react'
import {Row, Col, FormGroup, FormControl, Checkbox, DropdownButton, MenuItem} from 'react-bootstrap'
import GraphStore from './../stores/GraphStore'

const Knobs = React.createClass({

    getInitialState() {
        return {
            toSendFeatureCount: 0,
            toSendDisplayCount: 0,
            toSendPricePerUnit: 0
        }
    },

    componentWillReceiveProps(nextProps) {
        var self = this;
    },

    componentWillMount: function() {
        var self = this;
        this.setState({toSendFeatureCount: this.props.knobs.sum_feature_count.lower_limit});
        this.setState({toSendDisplayCount: this.props.knobs.sum_display_count.lower_limit});
        this.setState({toSendPricePerUnit: this.props.knobs.price_per_unit.lower_limit});
    },

    componentDidUpdate(prevProps, prevState) {
        if(prevProps && prevProps.knobs != this.props.knobs) {
            this.sendSliderData();
        }
    },

    sendSliderData() {
        if(GraphStore.getDirty()){
            GraphStore.sendSliderData({
                sum_feature_count: this.state.toSendFeatureCount,
                sum_display_count: this.state.toSendDisplayCount,
                price_per_unit: this.state.toSendPricePerUnit,
                subsegment: this.props.selectedValue
            });
        }
    },

    changeSendFeatureCount(event) {
        GraphStore.markDirty();
        event.persist()
        var self = this;
        this.setState({toSendFeatureCount: event.target.value}, function(){
            self.sendSliderData()
        });
    },

    changeSendDisplayCount(event) {
        GraphStore.markDirty();
        event.persist()
        var self = this;
        this.setState({toSendDisplayCount: event.target.value}, function(){
            self.sendSliderData()
        })
    },

    changeSendPricePerUnit(event){
        GraphStore.markDirty();
        event.persist()
        var self = this;
        this.setState({toSendPricePerUnit: event.target.value}, function(){
            self.sendSliderData()
        })
    },

    render () {
        var {knobs} = this.props;

        return <Col md={2} style={{padding: '0 32px'}}>
            <label>Feature count</label>
            <input type="range" onMouseUp={this.changeSendFeatureCount} min={knobs.sum_feature_count.lower_limit} max={knobs.sum_feature_count.upper_limit} step="0.0001" defaultValue={knobs.sum_feature_count.lower_limit}/>
            <label>Display count</label>
            <input type="range" onMouseUp={this.changeSendDisplayCount} min={knobs.sum_display_count.lower_limit} max={knobs.sum_feature_count.upper_limit} step="0.1" defaultValue={knobs.sum_display_count.lower_limit}/>
            <label>Price per unit</label>
            <input type="range" onMouseUp={this.changeSendPricePerUnit} min={knobs.price_per_unit.lower_limit} max={knobs.price_per_unit.upper_limit} step="0.01" defaultValue={knobs.price_per_unit.lower_limit}/>
        </Col>
    }
})

export default Knobs
