import Reflux from 'reflux'
import promises from './promises';

const GraphStore = Reflux.createStore({

    init: function() {
        this.data = {
            startDate: 156,
            endDate: 208,
            feature_count: [],
            price_per_unit: [],
            display_count: [],
            distribution: [],
            feature_share: [],
            display_share: [],
            unit_sales: [],
            volume_sales: [],
            volume_share: [],
            allData: null,
            knobs: {
                "price_per_unit": {},
                "sum_display_count": {},
                "sum_feature_count": {}
            },
            future_unit_sales: [],
            future_volume_sales: [],
            future_volume_share: [],
            markDirty: false
        };
    },

    getInitialState() {
        return this.data;
    },

    getAllData() {
        var self = this;
        return promises('get', 'data', null, function(res){
            self.allData = res.body.data;
            self.trigger(self.data);
        }, function(err){

        })
    },

    changeType(type) {
        var data = this.allData[type];
        this.data.feature_count = data["sum_feature_count"];
        this.data.price_per_unit = data["avg_price_per_unit"].map(function(item){
            return item * 100;
        });
        this.data.distribution = data["sum_distribution"].map(function(item){
            return item * 10000;
        });
        this.data.feature_share = data["sum_feature_share"].map(function(item){
            return item * 100;
        });
        this.data.display_share = data["sum_display_share"].map(function(item){
            return item * 100;
        });
        this.data.display_count = data["sum_display_count"];
        this.data.unit_sales = data["sum_unit_sales"];
        this.data.volume_sales = data["sum_volume_sales"];
        this.data.volume_share = data["sum_volume_share_of_category"].map(function(item, index){
            return item * 10000;
        });

        this.data.prediction_unit_sales = data["predicted_unit_sales"];
        this.data.prediction_volume_sales = data["predicted_volume_sales"];
        this.data.prediction_volume_share = data["predicted_volume_share_of_category"].map(function(item){
            return item * 100000;
        });

        this.data.knobs = data.knobs;
        this.trigger(this.data);
    },

    setDateRange(value) {
        this.data.startDate = value.min;
        this.data.endDate = value.max;
        this.trigger(this.data);
    },

    generateRawNumbers(num) {
        return _.range(0, num).map(function(item, index){
            return _.random(0, 100);
        })
    },

    getNumbers() {
        return this.data
    },

    sendSliderData(toSendData) {
        var self = this;
        return promises('post', 'predict', toSendData, function(res){
            var data = res.body.data;

            self.data.future_unit_sales = data.forecasted_unit_sales;
            self.data.future_volume_sales = data.forecasted_volume_sales;
            self.data.future_volume_share = data.forecasted_volume_share_of_category;
            self.trigger(self.data);
        }, function(err){

        })
    },

    markDirty() {
        this.data.markDirty = true;
        this.trigger(this.data);
    },

    getDirty() {
        return this.data.markDirty
    }
});

export default GraphStore
