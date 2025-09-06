

**Algorithm 1: BT Skeleton Generation and Consistency Validation**

```
Input: Natural language task description, Skill Manifest, Examples
Output: Verified BT skeleton

1: nodes ← LLM_Decompose(task, Skill_Manifest, examples)
2: nodes ← RAG_Existence_Check(nodes, Skill_DataStore)
3: repeat
4:     CFG, DFG ← Build_Graphs(nodes, Ontology)
5:     if Validate(CFG, DFG) == OK then
6:         return BT_Skeleton(nodes)
7:     else
8:         feedback ← Extract_Feedback(CFG, DFG, nodes)      
9:         candidates ← {}
10:        for each error in feedback do
11:            cands_error ← RAG_Retrieve(error.node, Skill_DataStore) 
12:            candidates[error.node] ← cands_error
13:        nodes ← LLM_Repair(nodes, candidates, feedback)     
14: until Validate(CFG, DFG) == OK

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
