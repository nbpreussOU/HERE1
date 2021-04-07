This document aims to give a generalized version of the code used in the creation of the network.

# Base Class

```
# calculates the wait time for a given node given constant time between patient arrivals
private function CALC_WAIT_TIME(float flow_in, float patients, int time_interval)
  wait = 0 
  for(int i = 0; i < flow_in; i++)
    wait += max(0, (time_interval/patients - time_interval/flow_in) * i
  return wait
  
# calculates the maximum wait time a single patient will experience at a given node  
private function CALC_MAX_SINGLE_PERSON_WAIT_TIME(float flow_in, float patients, int time_interval)
  wait = max(0, (time_interval/patients - time_interval/flow_in) * flow_in)    
  return wait
  
# calculates the number of patients who will experience a wait time greater than the maximum wait time  
private function LONG_WAIT(float flow_in, float patients, int time_interval, int max_wait)
  for(int i = 0; i < flow_in; i++)
    if (max(0, (time_interval / patients - time_interval / flowin) * k) > max_wait):
      return flowin - i
    return 0


CLASS Base_Model:
  public Base_Model()
    for n in nodes:
      initialize node to 1
    for e in edges:
      initialize edge to 1
    initialize all remaining variables to 1
    
  public function initialize()
    for n in nodes:
      n = poisson(lambda, 1)
    for each edge out of node n #alternatively can be done with multinomial variables
      edge out[capacity] = percentage * min(sum(edges in), n)
    graph = new graph()
    
  public function build_network()
    add nodes to graph
    add edges to graph
    add capacities to the edges of the graph
    
    for n in nodes
      for each edge out of n
        edge weight = CALC_MAX_SINGLE_PERSON_WAIT_TIME(sum(edges in), n, time interval)
    add weights to the the edges of the graph
      
  public function analyze_network()
    flow out = graph.calculate_maximum_flow(G, starting node, ending node)
    
    list edges = graph.longest_path(G, weight="weight")
    longest wait = 0
    for e in list edges
      longest wait += e[weight]
    
    efficiency = flow out/flow in
    
    total wait = 0
    for n in nodes
      for edge out of node n
        total wait += CALC_WAIT_TIME(edges in, n, time interval)
    
    return = [starting flow, flow out, efficiency, longest wait, total wait]
    
  public function draw_graph()
    change attributes of the graph to make it look pretty when you draw it
    draw it
    
  public function get_data()
    return[e in edges]
  
  public function set_data(edge data[])
    assign edge data to the edges
```

# Another Class

```
CLASS Modified_Model extends Base_Model
  
  public function Modified_Model()
    super()
    add new edge and node variables here
  
  @override
  public function initialize()
    super()
    initialize new edges and nodes as in the base class
    
  @override
  public function build_network()
    super()
    add new edges and nodes as in the base class
    
  you might need to modify other methods depending on the implementation, but it isn't strictly necessary
 ```     
