# Requirements
# graphviz

#In case it raised errors, uninstall graphvis and reinstall it
#! pip uninstall graphviz
#! conda install python-graphviz


from graphviz import Digraph, nohtml
import ast
import logging
import sys

# Data
# Provide tasks as list of tuples like:("Task id", "start", "duration", "end", "responsible", "predecessor)
# For the first tasks, predecessor will be "START", 
#   e.g., ("Task id", "start", "duration", "end", "responsible", "START")
# For the final tasks preced "END", 
#   e.g., ("END", "start", "duration", "end", "responsible", "Task id4"), ("END", "start", "duration", "end", "responsible", "Task id5")

def create_pert_chart(filename):
    task_list = []
    try:
        with open(filename) as f:
            for line in f:
                values = ast.literal_eval(line)
                task_list.append(values)
    except:
        logging.warning("Cannot generate PERT chart. File does not exist -> " + filename)
        sys.exit(1)
            
    a = task_list

    # Graph Instance
    g = Digraph('g', 
                filename='PERT.gv',
                node_attr={'shape': 'Mrecord', 
                           'height': '.1'})

    # configurations
    fill_color = 'grey93'

    g.attr(rankdir='LR')
    g.attr('node', shape='record')

    # Nodes

    for i in range(len(a)):
        if a[i][0] == "END":
                continue
        g.node(a[i][0], 
               nohtml('<f0>' + 
                      a[i][0] + 
                      ' |{' + a[i][1] + '|' + a[i][2] + '|' + a[i][3] + '}|<f2>' + 
                      a[i][4]), 
               fillcolor=fill_color, 
               style='filled',
               color='red'
              )

    # Edges
    '''
    g.edge('node0:f2', 'node4:f1') # connect edges with connetion points <f2> and <f1>
    g.edge('node0', 'node1')
    '''

    try:
        for i in a:
            #g.edge(i[3] + ':f2', i[0] + ':f0')
            if i[0] == "END":
                g.edge(i[5], "FINISH")
            else:
                g.edge(i[5], i[0])
    except:
        logging.info("Unexpected error. Check your inputs")
    finally:
        logging.info("PERT chart generated successfully")

    g.view()

if __name__ == '__main__':
    if len(sys.argv) >=2:
        filename = sys.argv[1] #"datafile.txt"
        create_pert_chart(filename)
    else:
        logging.info("Usage: pertchart <filename>")