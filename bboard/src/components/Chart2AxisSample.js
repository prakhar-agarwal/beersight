import React, { PropTypes } from 'react'
import ReactHighcharts from 'react-highcharts'
import _ from 'lodash'
import GraphStore from './../stores/GraphStore'
import Reflux from 'reflux'
import moment from 'moment'
import more from 'highcharts-more'

const Chart2AxisSample = React.createClass({

    getInitialState() {
        this._featureCountColor = '#333';
        this._unitSalesColor = '#F44336';
        this._volumeSalesColor = '#AB47BC';
        this._volumeShareColor = '#0288D1';
        this._predictColor = '#00BFA5';
        return null
    },

    render () {
        var startDate = moment('2013-01-06').add(this.props.startDate, 'weeks');
        var startPoint = Date.UTC(startDate.year(), startDate.month(), startDate.date());
        var weekDuration = 24 * 3600 * 1000 * 7;

        var predictionStartPoint = Date.UTC(2016, 8, 11);
        var futureStartPoint = Date.UTC(2016, 11, 25);

        var inputSeriesToShow = null;
        var inputSeriesName = "";
        switch (this.props.showInputValue) {
            case 'feature_count':
                inputSeriesToShow = this.props.featureCount;
                inputSeriesName = "Feature count"
                break;
            case 'price_per_unit':
                inputSeriesToShow = this.props.pricePerUnit;
                inputSeriesName = "Price per unit (cents)"
                break;
            case 'display_count':
                inputSeriesToShow = this.props.displayCount;
                inputSeriesName = "Display count"
                break;
            case 'feature_share':
                inputSeriesToShow = this.props.featureShare;
                inputSeriesName = "Feature share"
                break;
            case 'display_share':
                inputSeriesToShow = this.props.displayShare;
                inputSeriesName = "Display share"
                break;
            case 'distribution':
                inputSeriesToShow = this.props.distribution;
                inputSeriesName = "Distribution (BP)"
                break;
            default:
        }

        var config = {
            chart: {
                zoomType: 'x',
                animation: false
            },
            title: {
                text: ''
            },
            plotOptions: {
                column: {
                    pointPadding: 0,
                    borderWidth: 0,
                    pointWidth: 1,
                    groupPadding: 0
                }
            },
            xAxis: [{
                crosshair: true,
                type: 'datetime',
                dateTimeLabelFormats: {
                    day: '%e %b'
                }
            }],
            yAxis: [{
                title: {
                    text: inputSeriesName,
                    style: {
                        color: this._featureCountColor
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: this._featureCountColor
                    }
                },
                opposite: true,
                // max: 10000
            }],
            tooltip: {
                shared: true
            },
            legend: {
                enabled: false
            },
            series: []
        };

        config.series.push({
            name: inputSeriesName,
            type: 'column',
            data: inputSeriesToShow,
            animation: false,
            pointStart: startPoint,
            pointInterval: weekDuration,
            color: '#CFD8DC',
            maxPointWidth: 10,
            pointWidth: 5,
            pointPadding: 0,
            groupPadding: 0
        });
        // config.series.push({
        //     name: 'marker series',
        //     type: 'line',
        //     lineColor: 'transparent', /* makes line invisible */
        //     data: inputSeriesToShow, /* use nulls where you don't want arrowheads to appear */
        //     animation: false,
        //     pointStart: startPoint,
        //     pointInterval: weekDuration,
        //     showInLegend: false, /* will not show in legend */
        //     enableMouseTracking: false, /* users can't interact with the series */
        //     marker: {
        //         symbol: 'triangle',
        //         fillColor: 'rgba(0, 0, 0, 1)', /* match to the color of your column */
        //         radius: 1.5
        //     }
        // });

        if(this.props.showUnitSales === true) {
            config.yAxis.push({
                title: {
                    text: 'Unit sales',
                    style: {
                        color: this._unitSalesColor
                    }
                },
                labels: {
                    style: {
                        color: this._unitSalesColor
                    }
                },
                gridLineWidth: 0,
            });

            config.series.push({
                name: 'Unit Sales',
                type: 'line',
                yAxis: 1,
                data: this.props.unitSales,
                animation: false,
                pointStart: startPoint,
                pointInterval: weekDuration,
                color: this._unitSalesColor,
                marker: {
                    enabled: false
                },
                lineWidth: 3
            });

            config.series.push({
                name: 'Unit Sales prediction',
                type: 'line',
                yAxis: 1,
                data: this.props.predictionUnitSale,
                animation: false,
                pointStart: predictionStartPoint,
                pointInterval: weekDuration,
                color: this._unitSalesColor,
                marker: {
                    enabled: false
                },
                lineWidth: 5,
                dashStyle: 'ShortDot'
            });

            config.series.push({
                name: 'Unit Sales prediction',
                type: 'line',
                yAxis: 1,
                data: this.props.futureUnitSales,
                animation: false,
                pointStart: futureStartPoint,
                pointInterval: weekDuration,
                color: '#00BFA5',
                marker: {
                    enabled: false
                },
                lineWidth: 5,
                // dashStyle: 'ShortDot'
            });

        }

        if(this.props.showVolumeSales === true) {
            config.yAxis.push({
                title: {
                    text: 'Volume sales',
                    style: {
                        color: this._volumeSalesColor
                    }
                },
                labels: {
                    style: {
                        color: this._volumeSalesColor
                    }
                },
                gridLineWidth: 0,
            });

            config.series.push({
                name: 'Volume Sales',
                type: 'spline',
                yAxis: 1,
                data: this.props.volumeSales,
                animation: false,
                pointStart: startPoint,
                pointInterval: weekDuration,
                color: this._volumeSalesColor,
                marker: {
                    enabled: false
                }
            });
        }

        if(this.props.showVolumeShare === true) {
            config.yAxis.push({
                title: {
                    text: 'Volume share',
                    style: {
                        color: this._volumeShareColor
                    }
                },
                labels: {
                    style: {
                        color: this._volumeShareColor
                    }
                },
                gridLineWidth: 0,
            })

            config.series.push({
                name: 'Volume Share',
                type: 'spline',
                yAxis: 1,
                data: this.props.volumeShare,
                tooltip: {
                    valueSuffix: '%'
                },
                animation: false,
                pointStart: startPoint,
                pointInterval: weekDuration,
                color: this._volumeShareColor,
                marker: {
                    enabled: false
                }
            });
        }

        return <div>
            <ReactHighcharts config={config}/>
        </div>
    }
})

export default Chart2AxisSample
