

**Algorithm 1: BT Skeleton Generation and Consistency Validation**
```
Input:  Natural language task description, Skill DataStore (RAG), Examples
Output: Verified BT skeleton

1: repeat
2:     nodes ← LLM_Decompose(task, Examples)
3:     
4:     for each node in nodes do
5:         cand, score ← RAG_Retrieve(node, Skill_DataStore, Top=1)
6:         if score < θ then
7:             node ← cand
8:     
9:     CFG, DFG ← Build_Graphs(nodes, Ontology)
10:    feedback ← Validate(CFG, DFG)
11:    
12:    if feedback == NOK then
13:        candidates ← {}
14:        for each error in feedback do
15:            cands_error ← RAG_Retrieve(error.node, Skill_DataStore, Top=k)
16:            candidates[error.node] ← cands_error
17:        task ← Update_Task(task, candidates, feedback)
18: until feedback == OK
19: 
20: return BT_Skeleton(nodes)



```

**Algorithm 2: MCTS Parameter Optimization with Prior Update**

```
Input: Task description, Skill Manifest, Verified BT skeleton, Examples
Output: Optimized BT with parameters

1: priors ← LLM_Generate_Priors(task, Skill_Manifest, examples)
2: root ← Initialize_Root(priors)
3: for iteration = 1 ... N do
4:     path ← Selection(root, PUCT, priors)
5:     leaf ← Expansion(path)
6:     params ← Complete_Path(leaf, priors)
7:     reward ← Simulate(BT(params), Gazebo)
8:     Backpropagate(path, reward)
9:     if update_mode = "EMA" then
10:         priors ← EMA_Update(priors, reward)
11:     else if update_mode = "Bayesian" then
12:         priors ← Bayesian_Update(priors, reward)
13:     end if
14: end for
15: return Best_BT(root, priors)

```
