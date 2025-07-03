***New Start!!! ---Check about Argus***

## Four major conferences in the field of information security

- USENIX: USENIX Security
- S&P: IEEE Symposium on Security and Privacy
- CCS: ACM Conference on Computer and Communications Security 
- NDSS: Network and Distributed System Security Symposium

## Argus (Understanding and Bridging the Gap Between Unsupervised Network Representation Learning and Security Analytics)

* Unsupervised Network Representation Learning (UNRL)
* Graph security analytics (GSA) 
* discrete temporal graphs (DTG) 
* graph autoencoder (GAE)
* false positive rate (FPR)
* Message Passing Neural Networks (MPNNs) 

GJP: The Latest paper always covers the old guys!

### Graph Encoders

\[
H^{l+1} = \sigma\left(\tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}} H^l W^l\right)
\]

#### Each part

- **\(H^l\):** The features of all the nodes at layer \(l\) (a table of values for each node).
- **\(W^l\):** The trainable weight matrix for layer \(l\) (like in a regular neural network).
- **\(\tilde{A}\):** The adjacency matrix of the graph with added self-loops (so each node is also connected to itself).
- **\(\tilde{D}\):** The degree matrix (a diagonal matrix that tells how many edges each node has, including the self-loop).
- **\(\tilde{D}^{-\frac{1}{2}}\):** A normalization factor to scale the feature aggregation.
- **\(\sigma\):** An activation function, like ReLU, which adds non-linearity.

#### Step by Step

1. **Normalize the adjacency matrix:**  
   The normalization, \(\tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}}\), ensures that when you aggregate a node’s neighbors’ features, you don’t let high-degree nodes dominate.

2. **Aggregate neighbor features:**  
   Multiply the normalized adjacency matrix by the current node features (\(H^l\)). This means each node collects (averages or sums) features from its neighbors and itself.

3. **Apply weights:**  
   Multiply the result by \(W^l\). This is like a regular neural network layer, learning how to mix the features.

4. **Activate:**  
   Apply the activation function (\(\sigma\)), like ReLU, to introduce non-linearity.

#### What's an Activation Function

An **activation function** is a mathematical function used in neural networks (including Graph Convolutional Networks, or GCNs) to introduce non-linearity into the output of a layer. This allows the network to learn and model complex patterns in the data, rather than just simple linear relationships.

Examples:

1. **ReLU (Rectified Linear Unit):**
   \[
   \text{ReLU}(x) = \max(0, x)
   \]
   - Sets all negative values to zero and keeps positive values unchanged.
   - Very popular because it is simple and helps with the vanishing gradient problem.

2. **Sigmoid:**
   \[
   \sigma(x) = \frac{1}{1 + e^{-x}}
   \]
   - Squashes the input to a value between 0 and 1.
   - Was commonly used for binary classification and in early neural networks.

3. **Tanh (Hyperbolic Tangent):**
   \[
   \tanh(x) = \frac{e^{x} - e^{-x}}{e^{x} + e^{-x}}
   \]
   - Squashes the input to a value between -1 and 1.
   - Often used in recurrent neural networks.

**Actually**, it's quite a "mysterious" part of the Neural Networks()

### Issues and ARGUS's solutions

* Edge-feature loss -> a new encoder on top of MPNNs
* Gap betwwen link-prediction and attack-detection -> new loss function and redesigned downstream decoder
* Static graph modeling -> model the events as DTG

### Design of ARGUS













