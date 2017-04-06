angular.module('oddsFilters', [])
.filter('formatOdds', function() {
    return function(odds, oddsFormat, amount) {
        oddsFormat = oddsFormat.format;
        amount = amount.number;
        if (odds === "N/A"){return odds;};
        if (odds === 'None'){return '';}
        if (odds){
           if (oddsFormat === "Decimal" || oddsFormat === 'Implied Probability' || oddsFormat === 'Return On'){
               if(odds<0){
                   odds = -(100/odds)+1;
               }else if(odds>0){
                   odds = (odds/100)+1;
               }
               odds = parseFloat(odds).toFixed(2);
               if(oddsFormat === 'Implied Probability'){
                   odds = (1/odds)*100;
                   odds = odds.toFixed(1) +'%';
               }
                if(oddsFormat === 'Return On'){
                   odds = (odds*amount) - amount;
                   odds = parseInt(odds)+'$';
               }
           }
           else if (oddsFormat === 'American'){
               if(odds>0){
                   odds = '+'+odds;
               }
           }
           return odds;
        } else {
            return '';
        }
        
  };
});