'use strict';

(function($){

  $(function() {


    var own_data = [{"id":1,"name":"Administrator Uggeri","position_name":"Division Manager","chief_id":false},{"id":4,"name":"Elioenai Stone","position_name":"Assistant Division Manager","chief_id":1},{"id":5,"name":"Helmold McManus","position_name":"Asst. Stategic Planner Department Manager","chief_id":4},{"id":3,"name":"Ingvar Fekete","position_name":"Assistant Division Manager","chief_id":1},{"id":2,"name":"Jo Kramer","position_name":"Asst. Stategic Planner Department Manager","chief_id":1},{"id":6,"name":"Tiburcio Gibson","position_name":"Assistant Department Manager","chief_id":4}];

    
      
    var getTree = ( array) => {
      var roots = []
      var map = {};
      for(var i =0; i < array.length; i++){
          var node = array[i];
          node.children = [];
          map[node.id] = i; // use map to look-up the parents
          if (node.chief_id) {
              array[map[node.chief_id]].children.push(node);
          } else {
              roots.push(node);
          }
      }
      return roots[0];
    }

   



    var render = own_data => {
         console.log(own_data);
          var head_node_index =  own_data.findIndex( item => {
              return item.manager_id == false;
            } )
            console.log(getTree(own_data))
        
          var datascource = getTree(own_data)

          $('#chart-container').orgchart({
            'data' : datascource,
            'depth': 2,
            'nodeContent': 'position_name'
          });
    }

    // $.get('http://tripobsolution.com:9999/spc-employee/employee/', user_data => {
       render(own_data);
    // })
   

  });

})(jQuery);