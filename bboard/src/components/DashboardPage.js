import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import {Link} from 'react-router'
import {Row, Col, FormGroup, FormControl, Checkbox, DropdownButton, MenuItem} from 'react-bootstrap'
import {LinkContainer} from 'react-router-bootstrap'
import Slider from 'react-rangeslider'
import InputRange from 'react-input-range';
import moment from 'moment'

import Knobs from './Knobs'

import Chart2AxisSample from './Chart2AxisSample'
import GraphStore from './../stores/GraphStore'

import {RadioGroup, Radio} from 'react-radio-group'

const DashboardPage = React.createClass({

    mixins: [
        Reflux.connect(GraphStore, 'graph')
    ],

    getInitialState() {
        this._featureCountColor = '#333';
        this._unitSalesColor = '#F44336';
        this._volumeSalesColor = '#AB47BC';
        this._volumeShareColor = '#0288D1';

        return {
            showUnitSales: true,
            showVolumeSales: false,
            showVolumeShare: false,
            loading: true,
            showInputValue: 'feature_count',
            selectedValue: 'CRAFT',
            toSendFeatureCount: 0,
            toSendDisplayCount: 0,
            toSendPricePerUnit: 0
        }
    },

    componentWillMount: function() {
        self = this;
        GraphStore.getAllData().then(function(res){
            GraphStore.changeType("CRAFT");
            self.setState({loading: false})
        }, function(res){
            self.setState({loading: false})
        });
    },

    handleChange(value) {
        GraphStore.setDateRange(value);
    },

    handleInputChange(value) {
        this.setState({showInputValue: value})
    },

    formatLabel(value) {
        return moment('2013-01-06').add(value, 'weeks').format('DD MMM YYYY')
    },

    changeBeer(event) {
        event.persist()
        GraphStore.changeType(event.target.value);
        this.setState({selectedValue: event.target.value})
    },

    toggleUnitSales(event) {
        this.setState({showUnitSales: !this.state.showUnitSales})
    },

    toggleVolumeSales(event) {
        this.setState({showVolumeSales: !this.state.showVolumeSales})
    },

    toggleVolumeShare(event) {
        this.setState({showVolumeShare: !this.state.showVolumeShare})
    },

    render () {
        var {startDate, endDate, feature_count, price_per_unit, display_count, unit_sales, volume_sales, volume_share, prediction_unit_sales, prediction_volume_sales, prediction_volume_share_of_category, error_unit_sales, distribution, feature_share, display_share, knobs, future_unit_sales} = this.state.graph;

        return <div>
            <Row style={{padding: 12}}>
                <Col md={2} style={{padding: '0 32px'}}>
                    <FormGroup controlId="formControlsSelectMultiple">
                        <label>
                            Beer subsegment
                        </label>
                        <FormControl componentClass="select" onChange={this.changeBeer} ref="beerType" style={{background: '#3f51b5', color: '#FFF', border: 'none'}}>
                            <option value="CRAFT">Craft</option>
                            <option value="PREMIUM PLUS">Premium Plus</option>
                            <option value="VALUE LIGHT">Value Light</option>
                            <option value="PREMIUM LIGHT">Premium Light</option>
                            <option value="CORE IMPORT">Core Import</option>
                            <option value="VALUE REGULAR">Value Regular</option>
                            <option value="PREMIUM REGULAR">Premium Regular</option>
                            <option value="IMPORT">Import</option>
                        </FormControl>
                    </FormGroup>
                </Col>
                <Col md={8} style={{padding: '0 32px', paddingTop: 32}}>
                    <InputRange
                        formatLabel={this.formatLabel}
                        value={{min: startDate, max: endDate}}
                        onChange={this.handleChange}
                        maxValue={208} minValue={0}/>
                </Col>
                <Knobs knobs={knobs} selectedValue={this.state.selectedValue}/>
            </Row>
            <Row>
                <Col md={12}>
                    {
                        this.state.loading ? <div className="text-center" style={{background: '#ECEFF1', padding: 64}}>
                            Loading ...
                        </div> : <Chart2AxisSample
                            startDate={startDate}
                            endDate={endDate}
                            showInputValue={this.state.showInputValue}
                            featureCount={feature_count.slice(startDate, endDate)}
                            pricePerUnit={price_per_unit.slice(startDate, endDate)}
                            displayCount={display_count.slice(startDate, endDate)}
                            displayShare={display_share.slice(startDate, endDate)}
                            featureShare={feature_share.slice(startDate, endDate)}
                            distribution={feature_share.slice(startDate, endDate)}
                            unitSales={unit_sales.slice(startDate, endDate)}
                            volumeSales={volume_sales.slice(startDate, endDate)}
                            volumeShare={volume_share.slice(startDate, endDate)}
                            predictionUnitSale={prediction_unit_sales}
                            predictionVolumeSale={prediction_volume_sales}
                            predictionVolumeShare={prediction_volume_share_of_category}
                            futureUnitSales={future_unit_sales}
                            errorUnitSale={error_unit_sales}
                            showUnitSales={this.state.showUnitSales}
                            showVolumeSales={this.state.showVolumeSales}
                            showVolumeShare={this.state.showVolumeShare}/>
                    }
                </Col>
            </Row>
            <Row>
                <Col md={6} style={{padding: '0 12px 12px 12px'}}>
                    <FormGroup>
                        <label style={{padding: '0 24px', color: this._unitSalesColor}}>
                            <input
                            type="checkbox"
                            checked={this.state.showUnitSales}
                            onChange={this.toggleUnitSales} />
                            &nbsp;Unit Sales
                        </label><br></br>
                        <label style={{padding: '0 24px', color: this._volumeSalesColor}}>
                            <input
                            type="checkbox"
                            checked={this.state.showVolumeSales}
                            onChange={this.toggleVolumeSales} />
                        &nbsp;Volume Sales
                        </label><br></br>
                        <label style={{padding: '0 24px', color: this._volumeShareColor}}>
                            <input
                            type="checkbox"
                            checked={this.state.showVolumeShare}
                            onChange={this.toggleVolumeShare} />
                        &nbsp;Volume Share (in basis points)
                        </label>
                    </FormGroup>
                </Col>
                <Col md={6} style={{padding: 32, textAlign: 'right'}}>
                    <RadioGroup selectedValue={this.state.showInputValue} onChange={this.handleInputChange}>
                        <label>
                            <Radio value="feature_count" />&nbsp;Feature count
                        </label>
                        <br></br>
                        <label>
                            <Radio value="feature_share" />&nbsp;Feature Share
                        </label>
                        <br></br>
                        <label>
                            <Radio value="price_per_unit" />&nbsp;Price per unit
                        </label>
                        <br></br>
                        <label>
                            <Radio value="display_count" />&nbsp;Display count
                        </label>
                        <br></br>
                        <label>
                            <Radio value="display_share" />&nbsp;Display share
                        </label>
                        <br></br>
                        <label>
                            <Radio value="distribution" />&nbsp;Distribution (BP)
                        </label>
                        <br></br>
                    </RadioGroup>
                </Col>
            </Row>
        </div>
    }
})

export default DashboardPage;
