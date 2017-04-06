
var odds = angular.module('odds', ['oddsFilters', 'oddsDirectives', 'ngtimeago', 'highcharts-ng']);
odds.controller('OddsController', function($scope, $filter, $http) {
 
    $scope.sportsbooks = ['5Dimes', 'Bookmaker', 'BetDSI', 'Bovada', 'Pinnacle Sports', 'Sportbet', 'Sports Interaction', 'William Hill'];
    $scope.sportsbookNames = ['5Dimes', 'Bookmaker', 'BetDSI', 'Bovada', 'Pinnacle', 'Sportbet', 'Sports Inter.', 'William Hill'];
    $scope.sportsbookUrls = [
    'http://affiliates.5dimes.com/tracking/Affiliate.asp?AffID=AF0005643&mediaTypeID=220&AffUrlID=6536',
    'http://www.bookmaker.eu/bet-MMA?bc=fbn&cmpid=18390',
    'http://www.betdsi.eu/mma-betting?cmpid=18450',
    'http://record.bettingpartners.com/_pL3WIVtFNiquYRUFDWKk3WNd7ZgqdRLk/1/',
    'http://affiliates.sportbet.com/tracking/Affiliate.asp?AffID=AF0005643&mediaTypeID=220&AffUrlID=6536',
    'http://affiliate.sportsinteraction.com/processing/clickthrgh.asp?btag=a_8312b_840&aid=',
    'http://ads2.williamhill.com/redirect.aspx?pid=185253927&bid=1474211550&lpid=1470647208'
    ];
    
    $scope.betTypeCategories = ['straight', 'general props', 'distance props', 'fighter1 props', 'fighter2 props'];
    
    $scope.lastUpdated = function(lastUpdated){
        var date = new Date(lastUpdated);
        return $filter('timeago')(date);
    }
    
    $scope.oddsFormats = ['American', 'Decimal', 'Implied Probability', 'Return On'];
    $scope.oddsFormat = {format: $scope.oddsFormats[0]};
    
    $scope.event = event_odds;
    $scope.months = months;
    
    $scope.parlay = false;
    
    $scope.parlayBets = [];
    
    $scope.addToParlay = function(bet, sportsbook, odds){
        if($scope.parlay && odds){
            var betFound = $filter('filter')($scope.parlayBets, {bet:bet, sportsbook: sportsbook});
            if(betFound.length > 0){
                $scope.parlayBets.splice($scope.parlayBets.indexOf(betFound[0]), 1);
            } else {
                $scope.parlayBets.push({bet: bet, sportsbook: sportsbook, odds:odds});
            }
        };
    };
    
    $scope.updateParlay = function(){
        
        $scope.parlay = !$scope.parlay;
        if(!$scope.parlay){
            $scope.parlayBets = [];
        }
    };
    
    $scope.amount = {number: 10};
    
    $scope.totalParlay = function(){
        
        var odds;
        console.log()
        if($scope.parlayBets.length > 1){
            var parlayTotal = 1;
            for(var i=0; i<$scope.parlayBets.length; i++){
                parlayTotal = parlayTotal*$filter('formatOdds')($scope.parlayBets[i].odds, {format:'Decimal'}, $scope.amount);
            }
            if(parlayTotal == 2){
                odds = 100
            } else if(parlayTotal < 2){
                odds =  -100/(parlayTotal-1)
            } else if(parlayTotal > 2){
                odds = (parlayTotal-1)*100
            }
            odds = Math.round(odds);
        } else {
            odds = parseInt($scope.parlayBets[0].odds);
        }
        return $filter('formatOdds')(odds, $scope.oddsFormat, $scope.amount);
        
    }
    
    $scope.closeLineHistory = function(){
        $scope.lineHistoryStyle = {'display':'none'};
    }
    
    $scope.showLineHistory = function($event, bet, sportsbookName, betNo){
        if(!$scope.parlay){
            $scope.lineHistoryStyle = {'left':$event.pageX-300+'px', 'top':$event.pageY+10+'px', 'display':'block'};
        
        $scope.isLoading = true;
        //Get odds
        $http.get('/odds/line-history/'+bet.odds[sportsbookName].id).
              success(function(data, status, headers, config) {
                    var seriesData = [];
                    //data format [[timestamp, odds]]
                    for(var i=0; i<data.length; i++){
                        var timestamp = new Date(data[i].fields.timestamp);
                        seriesData.push([Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), timestamp.getDate(), timestamp.getHours(), timestamp.getMinutes()), data[i].fields['odds'+betNo]]);
                    }
                    $scope.lineLastUpdated = new Date(data[data.length - 1].fields.timestamp);
                    $scope.openOdds = data[0].fields['odds'+betNo];
                    $scope.currentOdds = data[data.length - 1].fields['odds'+betNo];
                    $scope.isLoading = false;
                    
                    $scope.chartConfig = {
                        options: {
                            chart : {
                                spacingLeft: 1,
                                spacingBottom:5,
                                spacingTop:25,
                                zoomType: 'x',
                                resetZoomButton: {
                                    position: { x: 0, y: -24 }
                                },
                                style: {
                                    fontFamily: 'Roboto'
                                }
                            },
                
                            credits: {
                                enabled: false
                            },
                            
                            tooltip: {
                                enabled:false
                            },
                            legend:{
                                enabled:false
                            },
                                
                            plotOptions: {
                                series: {
                                    marker: {
                                        states: {
                                            hover: {
                                                enabled: false
                                            }
                                        }
                                    }
                                },
                                line: {
                                    color: 'black'
                                }
                            },
                        },
                        series: [{
                            data: seriesData,
                            //name: name,
                            step: 'left',
                            type: 'line',
                            lineWidth: 2,
                            marker:{enabled:false}
                        }],
                        
                        title: {
                            text: ''
                        },
                        
                        xAxis: {
                            labels: {
                                style: {
                                    fontSize: 14
                                }
                            },
                            type: 'datetime',
                            dateTimeLabelFormats: { // don't display the dummy year
                                millisecond:"%b %e",
                                second:"%b %e",
                                minute:"%b %e",
                                hour:"%b %e",
                                day:"%b %e",
                                week:"%b %e",
                                month:"%b %e",
                                year:"%b %e"
                            }
                        },
                        yAxis: {
                            showFirstLabel:true,
                            showLastLabel:true,
                            maxPadding: 0.0,
                            minPadding: 0.0,
                            tickPositioner: function(min, max) {
            
                                var tickPositions = []
                                    tickPositions.push(min);
                                    tickPositions.push(max);
                                return tickPositions;
                            },
            
            
                            labels: {
                                y:5,
                                x:-5,
                                align:'right',
                                style: {
                                    fontSize: 14
                                },
                                formatter: function() {
                                    return $filter('formatOdds')(this.value, $scope.oddsFormat, $scope.amount)
                                }
                            },
            
                            title: {
                                text: ''
                            }
                        },
                
                        loading: false
                    }
                  
                  /*
                   var modalInstance = $modal.open({
                      templateUrl: "{% static "html/line-history.html" %}",
                      size: 'lg',
                      controller: 'LineHistoryController',
                      resolve: {
                         bet: function(){
                            return bet 
                         },
                         sportsbook: function(){
                            return sportsbookName 
                         },
                         betNo: function(){
                            return betNo 
                         },
                         odds: function(){
                             return data
                         },
                         oddsFormat: function(){
                             return $scope.oddsFormat;
                         }
                      }
                    });
                    */
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });
        }
        
        
    }
    
});

odds.controller('LineHistoryController', function($scope, bet, sportsbook, odds, betNo, oddsFormat) {
        var seriesData = [];
        //data format [[timestamp, odds]]
        for(var i=0; i<odds.length; i++){
            var timestamp = new Date(odds[i].fields.timestamp);
            seriesData.push([Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), timestamp.getDate(), timestamp.getHours(), timestamp.getMinutes()), odds[i].fields['odds'+betNo]]);
        }
        $scope.lastUpdated = new Date(odds[odds.length - 1].fields.timestamp);
        $scope.openOdds = odds[0].fields['odds'+betNo];
        $scope.currentOdds = odds[odds.length - 1].fields['odds'+betNo];
        $scope.betName = bet['bet'+betNo];
        $scope.sportsbook = sportsbook;
        
        $scope.chartConfig = {
            options: {
                chart : {
                    spacingLeft: 1,
                    spacingBottom:5,
                    spacingTop:25,
                    zoomType: 'x',
                    resetZoomButton: {
                        position: { x: 0, y: -24 }
                    }
                },
    
                credits: {
                    enabled: false
                },
                
                tooltip: {
                    enabled:false
                },
                legend:{
                    enabled:false
                },
                    
                plotOptions: {
                    series: {
                        marker: {
                            states: {
                                hover: {
                                    enabled: false
                                }
                            }
                        }
                    }
                },
            },
            series: [{
                data: seriesData,
                //name: name,
                step: 'left',
                type: 'line',
                lineWidth: 1,
                marker:{enabled:false}
            }],
            
            title: {
                text: ''
            },
            
            xAxis: {
                labels: {
                    style: {
                        fontSize: 14
                    }
                },
                type: 'datetime',
                dateTimeLabelFormats: { // don't display the dummy year
                    month: '%e. %b',
                    year: '%b'
                }
            },
            yAxis: {
                showFirstLabel:true,
                showLastLabel:true,
                maxPadding: 0.0,
                minPadding: 0.0,
                tickPositioner: function(min, max) {

                    var tickPositions = []
                        tickPositions.push(min);
                        tickPositions.push(max);
                    return tickPositions;
                },


                labels: {
                    y:5,
                    x:-5,
                    align:'right',
                    style: {
                        fontSize: 14
                    },
                    formatter: function() {
                        var oddsType = oddsFormat;
                        switch(oddsType)
                        {
                            case 'American':
                                if (this.value > 0){return '+'+this.value;} else { return this.value;}
                            case 'Decimal':
                                return this.value;
                            case 'Return On':
                                return '$'+this.value;
                            case 'Implied Probability':
                                return '% '+this.value;
                        }
                    }
                },

                title: {
                    text: ''
                }
            },
    
            loading: false
        }
        
});
