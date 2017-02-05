import Reflux from 'reflux'
import promises from './promises';

const UserStore = Reflux.createStore({

    init: function() {
        this.data = {

        };
    },

    getInitialState() {
        return this.data;
    },

    getUser() {
        var self = this;
        return promises('get', 'user', null, function(res){
            self.data = res.body;
            self.trigger(self.data);
        }, function(err){
            self.logoutUser();
        })

    }
});

export default UserStore
