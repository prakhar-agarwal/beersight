import requests from './RequestConfig';
import {browserHistory} from 'react-router'

var promises = function(type, url, data, success, error) {

    error = error || function() {};

    return new Promise(function(resolve, reject){
        var req = requests(type, url, data);

        if(type==='post' || type==='patch') {
            req.send(data) ;
        }

        req.end(function(err, res){
            if(err) {
                // TODO: handle 500 and 400 errors
                if(err.status == 400) {
                    browserHistory.push('/nomatch');
                }
                error(err);
                reject(err);
            } else {
                success(res);
                resolve(res);
            }
        });
    });
};

module.exports = promises;
