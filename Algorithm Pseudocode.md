

**Algorithm 1: BT Skeleton Generation and Consistency Validation**

```
Input: Natural language task description
Output: Verified BT skeleton

1: nodes ← LLM_Decompose(task, Skill_Manifest, examples)
2: nodes ← RAG_Existence_Check(nodes, Skill_DB)
3: repeat
4:     CFG, DFG ← Build_Graphs(nodes, Ontology)
5:     if Validate(CFG, DFG) == OK then
6:         return BT_Skeleton(nodes)
7:     else
8:         candidates ← RAG_Retrieve(nodes, Skill_DB)
9:         nodes ← LLM_Repair(nodes, candidates)
10: until Validate(CFG, DFG) == OK
```

**Algorithm 2: MCTS Parameter Optimization with Prior Update**

```
Input: Verified BT skeleton, Priors from LLM
Output: Optimized BT with parameters

1: Initialize root node with priors
2: for iteration = 1 ... N do
3:     path ← Selection(root, PUCT)
4:     leaf ← Expansion(path)
5:     params ← Complete_Path(leaf, priors)
6:     reward ← Simulate(BT(params), Gazebo)
7:     Backpropagate(path, reward)
8:     Update_Priors(priors, reward, EMA or Bayesian)
9: end for
10: return Best_BT(priors)
```
