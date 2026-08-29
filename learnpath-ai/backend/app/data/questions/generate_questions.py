import json
import os

def generate_domain_file(filename, questions):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2)
    print(f"Generated {filename} with {len(questions)} questions.")

# 1. MACHINE LEARNING QUESTIONS
ml_questions = [
    # Python for ML
    {
        "id": "ml_python_001",
        "domain": "machine_learning",
        "skill": "Python for ML",
        "difficulty": "easy",
        "question": "Which Python library is primarily used for providing high-performance multidimensional array objects and tools for working with them?",
        "options": [
            {"id": "A", "text": "Pandas"},
            {"id": "B", "text": "NumPy"},
            {"id": "C", "text": "Scikit-Learn"},
            {"id": "D", "text": "Matplotlib"}
        ],
        "correct_option_id": "B",
        "explanation": "NumPy is the fundamental package for scientific computing in Python, providing support for large, multi-dimensional arrays and matrices.",
        "weight": 1
    },
    {
        "id": "ml_python_002",
        "domain": "machine_learning",
        "skill": "Python for ML",
        "difficulty": "medium",
        "question": "In Scikit-Learn, what is the key difference between calling fit() and fit_transform() on a data preprocessor object like StandardScaler?",
        "options": [
            {"id": "A", "text": "fit() calculates parameters and applies them, while fit_transform() only calculates parameters."},
            {"id": "B", "text": "fit() only calculates the mean and variance parameters, while fit_transform() calculates them and applies the transformation to return scaled data."},
            {"id": "C", "text": "fit() is used for training labels, while fit_transform() is only used for training features."},
            {"id": "D", "text": "There is no difference; they are exact aliases of each other."}
        ],
        "correct_option_id": "B",
        "explanation": "fit() computes the parameters (e.g. mean, std dev for StandardScaler) and stores them as internal state. fit_transform() computes the parameters AND applies the scaling transformation, returning the transformed array.",
        "weight": 1
    },
    {
        "id": "ml_python_003",
        "domain": "machine_learning",
        "skill": "Python for ML",
        "difficulty": "hard",
        "question": "You are training a large neural network in PyTorch and want to optimize GPU memory utilization during validation. Which action is most appropriate?",
        "options": [
            {"id": "A", "text": "Run code inside a `with torch.no_grad():` block to disable gradient computation and free up cache memory."},
            {"id": "B", "text": "Manually delete all model parameters using `del model` before validation starts."},
            {"id": "C", "text": "Set the learning rate to zero during validation."},
            {"id": "D", "text": "Call `loss.backward()` inside the validation loop to flush the computational graph."}
        ],
        "correct_option_id": "A",
        "explanation": "`torch.no_grad()` disables gradient tracking, which prevents the building of the dynamic computation graph, significantly reducing memory consumption during inference/validation.",
        "weight": 1
    },

    # Data Preprocessing
    {
        "id": "ml_prep_001",
        "domain": "machine_learning",
        "skill": "Data Preprocessing",
        "difficulty": "easy",
        "question": "Which encoding technique represents categorical features as binary vectors where only one index is hot?",
        "options": [
            {"id": "A", "text": "Ordinal Encoding"},
            {"id": "B", "text": "Label Encoding"},
            {"id": "C", "text": "One-Hot Encoding"},
            {"id": "D", "text": "Target Encoding"}
        ],
        "correct_option_id": "C",
        "explanation": "One-hot encoding creates a binary column for each category, setting exactly one column to 1 (hot) and the others to 0.",
        "weight": 1
    },
    {
        "id": "ml_prep_002",
        "domain": "machine_learning",
        "skill": "Data Preprocessing",
        "difficulty": "medium",
        "question": "When preprocessing data for a Distance-based algorithm like K-Nearest Neighbors (KNN), why is scaling features crucial?",
        "options": [
            {"id": "A", "text": "Unscaled features will cause the algorithm to run out of memory during calculations."},
            {"id": "B", "text": "Features with larger magnitudes will dominate the distance metric, making other features irrelevant."},
            {"id": "C", "text": "Scaling categorical variables is required before applying distance computations."},
            {"id": "D", "text": "Scaling shifts feature distribution to perfectly match a binomial distribution."}
        ],
        "correct_option_id": "B",
        "explanation": "KNN uses distance measures like Euclidean distance. Unscaled features with high values will dominate the distance calculation compared to features with small numeric ranges.",
        "weight": 1
    },
    {
        "id": "ml_prep_003",
        "domain": "machine_learning",
        "skill": "Data Preprocessing",
        "difficulty": "hard",
        "question": "You have a dataset with a highly skewed continuous target variable (e.g. house prices). How should you preprocess the target variable before training a linear regression model?",
        "options": [
            {"id": "A", "text": "Apply a logarithmic transformation to the target variable to stabilize variance and normalize distributions, and apply exp() during inference."},
            {"id": "B", "text": "Impute the target variable using the median value to remove the skew."},
            {"id": "C", "text": "One-hot encode the continuous price ranges to treat them as nominal values."},
            {"id": "D", "text": "Use min-max scaling to compress the range strictly between 0 and 1, ignoring the skewness."}
        ],
        "correct_option_id": "A",
        "explanation": "Linear regression performs best when the target variable distribution is normal. Transforming it via logarithm helps handle extreme skewness and stabilizes residuals variance. Exponentiation reverses the prediction to original scale during inference.",
        "weight": 1
    },

    # Statistics & Probability
    {
        "id": "ml_stats_001",
        "domain": "machine_learning",
        "skill": "Statistics & Probability",
        "difficulty": "easy",
        "question": "What does the Central Limit Theorem state about the sampling distribution of the sample mean as sample size increases?",
        "options": [
            {"id": "A", "text": "It will always follow a uniform distribution."},
            {"id": "B", "text": "It will follow a normal distribution, regardless of the shape of the population distribution."},
            {"id": "C", "text": "It will match the exact distribution of the population."},
            {"id": "D", "text": "It will have a variance equal to the standard deviation."}
        ],
        "correct_option_id": "B",
        "explanation": "The CLT states that the sample mean distribution approaches a normal distribution as sample size increases, even if the parent population distribution is non-normal.",
        "weight": 1
    },
    {
        "id": "ml_stats_002",
        "domain": "machine_learning",
        "skill": "Statistics & Probability",
        "difficulty": "medium",
        "question": "Which term describes the probability of rejecting the null hypothesis when it is actually true (Type I error)?",
        "options": [
            {"id": "A", "text": "Statistical Power (1 - Beta)"},
            {"id": "B", "text": "Significance Level (Alpha)"},
            {"id": "C", "text": "Margin of Error"},
            {"id": "D", "text": "Confidence Level (1 - Alpha)"}
        ],
        "correct_option_id": "B",
        "explanation": "The significance level alpha is the probability of committing a Type I error (incorrectly rejecting a true null hypothesis).",
        "weight": 1
    },
    {
        "id": "ml_stats_003",
        "domain": "machine_learning",
        "skill": "Statistics & Probability",
        "difficulty": "hard",
        "question": "Under what condition is Naive Bayes' assumption of class conditional independence violated in practice, and how does it affect predictions?",
        "options": [
            {"id": "A", "text": "When features are highly correlated; this leads to overconfident predictions near 0 or 1, although classification ranking remains relatively robust."},
            {"id": "B", "text": "When the dataset is small, causing the probability distributions to fail to converge."},
            {"id": "C", "text": "When the target classes are highly unbalanced, causing the prior probability of the minority class to drift to zero."},
            {"id": "D", "text": "When data is normalized, which violates the gaussian assumption of numerical features."}
        ],
        "correct_option_id": "A",
        "explanation": "Naive Bayes assumes all features are independent given the class. If features are correlated, they double-count evidence, resulting in posterior probabilities pushed excessively toward 0 or 1, though the model ranking predictions can remain highly accurate.",
        "weight": 1
    },

    # Regression
    {
        "id": "ml_regr_001",
        "domain": "machine_learning",
        "skill": "Regression",
        "difficulty": "easy",
        "question": "Which loss function is minimized in ordinary least squares (OLS) linear regression?",
        "options": [
            {"id": "A", "text": "Mean Absolute Error (MAE)"},
            {"id": "B", "text": "Mean Squared Error (MSE)"},
            {"id": "C", "text": "Cross-Entropy Loss"},
            {"id": "D", "text": "Hinge Loss"}
        ],
        "correct_option_id": "B",
        "explanation": "OLS regression minimizes the sum of squared residuals, which directly equates to minimizing Mean Squared Error (MSE).",
        "weight": 1
    },
    {
        "id": "ml_regr_002",
        "domain": "machine_learning",
        "skill": "Regression",
        "difficulty": "medium",
        "question": "What is the primary difference in regularization effect between Lasso (L1) and Ridge (L2) regression?",
        "options": [
            {"id": "A", "text": "Lasso shrinks coefficients to exactly zero (feature selection), while Ridge shrinks them close to zero but not exactly zero."},
            {"id": "B", "text": "Lasso only works on linear regression, while Ridge is designed for logistic regression."},
            {"id": "C", "text": "Ridge performs automatic feature selection, whereas Lasso shrinks all weights uniformly."},
            {"id": "D", "text": "Lasso increases model complexity, while Ridge reduces it."}
        ],
        "correct_option_id": "A",
        "explanation": "Lasso (L1) adds a penalty proportional to the absolute values of the coefficients, causing some coefficients to become exactly 0. Ridge (L2) uses squared values penalty, shrinking them asymptotically close to 0.",
        "weight": 1
    },
    {
        "id": "ml_regr_003",
        "domain": "machine_learning",
        "skill": "Regression",
        "difficulty": "hard",
        "question": "A linear regression model has high R-squared on training data, but low R-squared on test data. Multicollinearity is detected. Which approach will resolve this issues best?",
        "options": [
            {"id": "A", "text": "Add polynomial terms for all features to increase the capacity of the model."},
            {"id": "B", "text": "Remove highly correlated features or apply Ridge/Lasso regularization to penalize large weights."},
            {"id": "C", "text": "Change the loss metric from MSE to MAE."},
            {"id": "D", "text": "Increase the learning rate of the optimization step."}
        ],
        "correct_option_id": "B",
        "explanation": "Multicollinearity inflates coefficient variance, leading to overfitting. Dropping redundant features or utilizing L1/L2 regularization stabilizes the coefficient estimations, improving generalization.",
        "weight": 1
    },

    # Classification
    {
        "id": "ml_class_001",
        "domain": "machine_learning",
        "skill": "Classification",
        "difficulty": "easy",
        "question": "Which function is used to map real-valued output predictions of a linear model to a probability score between 0 and 1 in logistic regression?",
        "options": [
            {"id": "A", "text": "ReLU function"},
            {"id": "B", "text": "Sigmoid (Logistic) function"},
            {"id": "C", "text": "Hyperbolic Tangent (tanh)"},
            {"id": "D", "text": "Softmax function"}
        ],
        "correct_option_id": "B",
        "explanation": "The sigmoid function maps any real value into a range between 0 and 1, representing the probability of the positive class.",
        "weight": 1
    },
    {
        "id": "ml_class_002",
        "domain": "machine_learning",
        "skill": "Classification",
        "difficulty": "medium",
        "question": "For a classification task, when is using F1-Score preferred over standard Accuracy as the main evaluation metric?",
        "options": [
            {"id": "A", "text": "When the classes are balanced and the cost of false positives is extremely low."},
            {"id": "B", "text": "When dealing with imbalanced datasets where the cost of false positives and false negatives is highly unequal or critical."},
            {"id": "C", "text": "When you want to evaluate continuous regression targets."},
            {"id": "D", "text": "Only when training on random forests or decision tree architectures."}
        ],
        "correct_option_id": "B",
        "explanation": "F1-Score is the harmonic mean of precision and recall. Accuracy is misleading when classes are highly imbalanced (e.g. 99% majority class), whereas F1 focus is on the performance on the minority class.",
        "weight": 1
    },
    {
        "id": "ml_class_003",
        "domain": "machine_learning",
        "skill": "Classification",
        "difficulty": "hard",
        "question": "In Support Vector Machines (SVM), how does the choice of a radial basis function (RBF) kernel parameter gamma (high vs low) affect model complexity?",
        "options": [
            {"id": "A", "text": "High gamma means a single training sample has a close range of influence, leading to overfitting; low gamma means a wide range of influence, leading to underfitting."},
            {"id": "B", "text": "High gamma makes the decision boundary linear, while low gamma makes it highly non-linear."},
            {"id": "C", "text": "Gamma does not affect complexity; it only adjusts the scale of the target label."},
            {"id": "D", "text": "High gamma reduces computation time by simplifying the support vectors."}
        ],
        "correct_option_id": "A",
        "explanation": "Gamma determines the radius of influence of individual support vectors. High gamma values mean support vectors have localized influence, causing tight fitting around samples (overfitting). Low values mean broader influence, leading to smoother boundaries (underfitting).",
        "weight": 1
    },

    # Feature Engineering
    {
        "id": "ml_feat_001",
        "domain": "machine_learning",
        "skill": "Feature Engineering",
        "difficulty": "easy",
        "question": "What is the primary objective of Principal Component Analysis (PCA)?",
        "options": [
            {"id": "A", "text": "To increase the number of features in a dataset"},
            {"id": "B", "text": "To perform linear regression scaling"},
            {"id": "C", "text": "To reduce the dimensionality of the dataset while preserving most variance"},
            {"id": "D", "text": "To automatically detect target categories"}
        ],
        "correct_option_id": "C",
        "explanation": "PCA is an unsupervised dimensionality reduction technique that projects features into orthogonal directions of maximum variance.",
        "weight": 1
    },
    {
        "id": "ml_feat_002",
        "domain": "machine_learning",
        "skill": "Feature Engineering",
        "difficulty": "medium",
        "question": "Which technique would be most appropriate to handle a high-cardinality categorical feature (e.g., zip code) in a predictive gradient boosting model?",
        "options": [
            {"id": "A", "text": "Apply One-Hot Encoding to create thousands of columns."},
            {"id": "B", "text": "Use Target Encoding (with regularization/smoothing) to map categories to the target mean."},
            {"id": "C", "text": "Min-max scale the categorical strings alphabetically."},
            {"id": "D", "text": "Drop the column entirely, since categorical variables cannot be used in trees."}
        ],
        "correct_option_id": "B",
        "explanation": "Target Encoding maps categories to target values. For high-cardinality features, One-Hot Encoding creates high dimensionality (sparse matrices), causing trees to perform poorly. Target encoding with smoothing resolves this cleanly.",
        "weight": 1
    },
    {
        "id": "ml_feat_003",
        "domain": "machine_learning",
        "skill": "Feature Engineering",
        "difficulty": "hard",
        "question": "What is a primary risk of using target encoding on categorical features, and how is it typically mitigated?",
        "options": [
            {"id": "A", "text": "It risks target leakage (overfitting); it is mitigated by adding smoothing and using out-of-fold target averages (e.g., via K-Fold)."},
            {"id": "B", "text": "It risks underfitting; it is mitigated by duplicating rows to increase dataset volume."},
            {"id": "C", "text": "It risks multicollinearity; it is mitigated by running PCA immediately after target encoding."},
            {"id": "D", "text": "It risks numerical instability; it is mitigated by multiplying values by zero."}
        ],
        "correct_option_id": "A",
        "explanation": "Target encoding directly uses the target label to calculate averages for categories, creating massive target leakage. Mitigations include adding noise (smoothing) and calculating averages out-of-fold (using cross-validation subsets).",
        "weight": 1
    },

    # Model Evaluation
    {
        "id": "ml_eval_001",
        "domain": "machine_learning",
        "skill": "Model Evaluation",
        "difficulty": "easy",
        "question": "What does a Confusion Matrix help visualize?",
        "options": [
            {"id": "A", "text": "The gradient descent steps over epochs"},
            {"id": "B", "text": "Feature importances of a random forest"},
            {"id": "C", "text": "Actual versus predicted class distributions for a classifier"},
            {"id": "D", "text": "The memory consumption of train vs validation splits"}
        ],
        "correct_option_id": "C",
        "explanation": "A confusion matrix shows the counts of true positives, true negatives, false positives, and false negatives for classification evaluations.",
        "weight": 1
    },
    {
        "id": "ml_eval_002",
        "domain": "machine_learning",
        "skill": "Model Evaluation",
        "difficulty": "medium",
        "question": "How does K-Fold Cross-Validation provide a better estimate of model generalization performance than a single Train/Test split?",
        "options": [
            {"id": "A", "text": "It trains the model on the test data to guarantee high test metrics."},
            {"id": "B", "text": "It runs the training process in parallel to double the learning rate."},
            {"id": "C", "text": "It uses multiple different splits iteratively, ensuring that every data point is used for both training and validation once."},
            {"id": "D", "text": "It automatically prunes redundant model features at each fold."}
        ],
        "correct_option_id": "C",
        "explanation": "K-fold cross-validation splits data into K subsets. It trains K times, using each fold as a validation set once, providing a distribution of validation scores with low variance.",
        "weight": 1
    },
    {
        "id": "ml_eval_003",
        "domain": "machine_learning",
        "skill": "Model Evaluation",
        "difficulty": "hard",
        "question": "You are building a diagnostic tool to identify a rare disease. A false negative (missing a sick patient) is far more costly than a false positive. Which metric should you optimize, and how does it affect the decision threshold?",
        "options": [
            {"id": "A", "text": "Optimize Recall (Sensitivity); decrease the probability decision threshold below 0.5."},
            {"id": "B", "text": "Optimize Precision; increase the probability decision threshold to 0.9."},
            {"id": "C", "text": "Optimize Accuracy; keep the threshold at exactly 0.5."},
            {"id": "D", "text": "Optimize Specificity; increase the threshold to 0.7."}
        ],
        "correct_option_id": "A",
        "explanation": "To minimize false negatives, you need to maximize Recall (Recall = TP / (TP + FN)). Lowering the decision threshold below 0.5 classifies more patients as positive, catching more sick patients at the cost of some additional false positives.",
        "weight": 1
    },

    # Ensemble Learning
    {
        "id": "ml_ens_001",
        "domain": "machine_learning",
        "skill": "Ensemble Learning",
        "difficulty": "easy",
        "question": "Which ensemble technique fits multiple independent decision trees in parallel on bootstrapped subsets of training data?",
        "options": [
            {"id": "A", "text": "AdaBoost"},
            {"id": "B", "text": "Gradient Boosting"},
            {"id": "C", "text": "Random Forest"},
            {"id": "D", "text": "Stacking"}
        ],
        "correct_option_id": "C",
        "explanation": "Random Forest builds independent decision trees in parallel using bootstrapping (bagging) and random feature selection.",
        "weight": 1
    },
    {
        "id": "ml_ens_002",
        "domain": "machine_learning",
        "skill": "Ensemble Learning",
        "difficulty": "medium",
        "question": "What is the key difference in training strategy between Bagging and Boosting algorithms?",
        "options": [
            {"id": "A", "text": "Bagging fits models sequentially to correct errors, while Boosting fits models in parallel independently."},
            {"id": "B", "text": "Bagging builds independent models in parallel, while Boosting builds models sequentially where each new model corrects previous errors."},
            {"id": "C", "text": "Bagging is only used for neural networks, whereas Boosting is used for linear regression."},
            {"id": "D", "text": "Bagging increases model bias, while Boosting decreases model variance."}
        ],
        "correct_option_id": "B",
        "explanation": "Bagging (Bootstrap Aggregating) trains models independently in parallel (e.g. Random Forest). Boosting trains models sequentially (e.g. XGBoost), focusing on sample weights or residuals missed by predecessor models.",
        "weight": 1
    },
    {
        "id": "ml_ens_003",
        "domain": "machine_learning",
        "skill": "Ensemble Learning",
        "difficulty": "hard",
        "question": "How do Gradient Boosting Trees (GBDT) handle the bias-variance tradeoff differently as the number of estimators (trees) increases compared to Random Forests?",
        "options": [
            {"id": "A", "text": "Random Forests overfit heavily as the number of trees increases; GBDTs maintain a constant variance because trees are sequential."},
            {"id": "B", "text": "Adding trees to Random Forests reduces variance without increasing bias (doesn't overfit easily); adding trees to GBDTs continues to reduce training bias and can easily lead to overfitting (variance increases)."},
            {"id": "C", "text": "GBDTs reduce variance through averaging, while Random Forests reduce bias through boosting."},
            {"id": "D", "text": "Both architectures respond identically, overfitting at exactly the same rate as trees are added."}
        ],
        "correct_option_id": "B",
        "explanation": "In Random Forest, averaging independent trees reduces variance but cannot overfit by adding more trees (generalization error plateaus). GBDTs minimize residuals sequentially, so adding too many trees will cause the model to eventually fit sample noise (overfit).",
        "weight": 1
    },

    # Unsupervised Learning
    {
        "id": "ml_unsup_001",
        "domain": "machine_learning",
        "skill": "Unsupervised Learning",
        "difficulty": "easy",
        "question": "Which clustering algorithm groups data points by iteratively assigning them to the nearest centroid and recalculating the centroid position?",
        "options": [
            {"id": "A", "text": "DBSCAN"},
            {"id": "B", "text": "K-Means Clustering"},
            {"id": "C", "text": "Hierarchical Clustering"},
            {"id": "D", "text": "Isolation Forest"}
        ],
        "correct_option_id": "B",
        "explanation": "K-Means is a classic centroid-based clustering algorithm that alternates assignment and update steps.",
        "weight": 1
    },
    {
        "id": "ml_unsup_002",
        "domain": "machine_learning",
        "skill": "Unsupervised Learning",
        "difficulty": "medium",
        "question": "When comparing K-Means and DBSCAN clustering, which is a major advantage of DBSCAN?",
        "options": [
            {"id": "A", "text": "DBSCAN requires you to specify the number of clusters (K) in advance."},
            {"id": "B", "text": "DBSCAN can find arbitrarily shaped clusters and naturally identifies outlier noise points."},
            {"id": "C", "text": "DBSCAN uses linear projections to guarantee cluster separation."},
            {"id": "D", "text": "DBSCAN is computationally faster on highly high-dimensional datasets."}
        ],
        "correct_option_id": "B",
        "explanation": "Unlike K-Means (which forms spherical clusters and forces every point into a cluster), DBSCAN identifies clusters based on density, allowing arbitrary shapes and designating sparse points as noise (-1).",
        "weight": 1
    },
    {
        "id": "ml_unsup_003",
        "domain": "machine_learning",
        "skill": "Unsupervised Learning",
        "difficulty": "hard",
        "question": "Explain the 'curse of dimensionality' in the context of distance-based clustering algorithms like K-Means.",
        "options": [
            {"id": "A", "text": "As dimensions increase, distance values become smaller, causing K-Means to divide by zero."},
            {"id": "B", "text": "As dimensionality increases, the distance between any two points in the high-dimensional space converges to the same value, rendering distance metrics ineffective."},
            {"id": "C", "text": "High dimensions cause features to become highly dependent on target classes."},
            {"id": "D", "text": "High-dimensional spaces cause the cluster centroids to shift outside the convex hull of the dataset."}
        ],
        "correct_option_id": "B",
        "explanation": "In high-dimensional spaces, data points become extremely sparse. The ratio between the distance to the nearest point and the distance to the farthest point approaches 1, meaning all points appear almost equidistant from one another, breaking distance-based algorithms.",
        "weight": 1
    },

    # Model Deployment
    {
        "id": "ml_deploy_001",
        "domain": "machine_learning",
        "skill": "Model Deployment",
        "difficulty": "easy",
        "question": "Which Python library is standard for serializing model objects to disk so they can be loaded later in production?",
        "options": [
            {"id": "A", "text": "Pickle (or Joblib)"},
            {"id": "B", "text": "JSON"},
            {"id": "C", "text": "Requests"},
            {"id": "D", "text": "NumPy"}
        ],
        "correct_option_id": "A",
        "explanation": "Pickle or Joblib serialize Python objects (like trained models) into a byte stream on disk, facilitating fast loading.",
        "weight": 1
    },
    {
        "id": "ml_deploy_002",
        "domain": "machine_learning",
        "skill": "Model Deployment",
        "difficulty": "medium",
        "question": "What is the primary benefit of deploying a model as a REST API microservice (e.g. using FastAPI) compared to embedded deployment in the main application codebase?",
        "options": [
            {"id": "A", "text": "FastAPI guarantees the model uses 100% CPU capacity."},
            {"id": "B", "text": "It decouples the model lifecycle, permitting independent updates and scalability without affecting the main client application."},
            {"id": "C", "text": "FastAPI automatically translates models to WebAssembly."},
            {"id": "D", "text": "It eliminates latency entirely during prediction requests."}
        ],
        "correct_option_id": "B",
        "explanation": "Decoupling model deployment as an independent API microservice means changes/versions of models can be deployed without deploying the parent application, and model instances can be scaled horizontally.",
        "weight": 1
    },
    {
        "id": "ml_deploy_003",
        "domain": "machine_learning",
        "skill": "Model Deployment",
        "difficulty": "hard",
        "question": "What is 'data drift' in production ML deployment, and how is it typically monitored and resolved?",
        "options": [
            {"id": "A", "text": "It is when model code modifications are pushed directly to main; resolved by using Git branches."},
            {"id": "B", "text": "It is a shift in the statistical distribution of input feature data compared to training data over time; resolved by monitoring features (e.g. KS test) and retraining the model on newer data."},
            {"id": "C", "text": "It is the loss of database records due to server crashes; resolved by implementing daily backups."},
            {"id": "D", "text": "It is when predictions slow down; resolved by increasing system RAM."}
        ],
        "correct_option_id": "B",
        "explanation": "Data drift occurs when production input feature distributions diverge from training distributions. Monitoring tools compare statistical distributions (using Kolmogorov-Smirnov test, Population Stability Index) to alert engineers to retrain.",
        "weight": 1
    }
]

# 2. DATA SCIENCE QUESTIONS
ds_questions = [
    # Python
    {
        "id": "ds_python_001",
        "domain": "data_science",
        "skill": "Python",
        "difficulty": "easy",
        "question": "Which Python data structure represents an unordered, mutable collection of unique elements?",
        "options": [
            {"id": "A", "text": "List"},
            {"id": "B", "text": "Tuple"},
            {"id": "C", "text": "Set"},
            {"id": "D", "text": "Dictionary"}
        ],
        "correct_option_id": "C",
        "explanation": "Sets in Python store unique, unordered items and provide fast membership testing.",
        "weight": 1
    },
    {
        "id": "ds_python_002",
        "domain": "data_science",
        "skill": "Python",
        "difficulty": "medium",
        "question": "What is the key difference between list.sort() and the sorted() function in Python?",
        "options": [
            {"id": "A", "text": "list.sort() modifies the list in-place and returns None, whereas sorted() returns a new sorted list, leaving the original list unchanged."},
            {"id": "B", "text": "list.sort() is faster because it compiles to C, while sorted() is written in pure Python."},
            {"id": "C", "text": "sorted() only works on dictionaries, while list.sort() only works on lists."},
            {"id": "D", "text": "There is no difference; they are interchangeable."}
        ],
        "correct_option_id": "A",
        "explanation": "list.sort() is a method of list class that operates in-place (mutates target). sorted() is a built-in function that takes any iterable and returns a new list copy.",
        "weight": 1
    },
    {
        "id": "ds_python_003",
        "domain": "data_science",
        "skill": "Python",
        "difficulty": "hard",
        "question": "What is the behavior of the Global Interpreter Lock (GIL) in standard CPython implementation during multi-threaded CPU-bound operations?",
        "options": [
            {"id": "A", "text": "The GIL enables true multi-core parallel processing for CPU-bound tasks automatically."},
            {"id": "B", "text": "The GIL restricts execution to exactly one native thread at a time, preventing multi-threaded Python code from fully utilizing multiple CPU cores for CPU-bound tasks."},
            {"id": "C", "text": "The GIL locks memory allocations to prevent imports from leaking memory blocks."},
            {"id": "D", "text": "The GIL disables async execution routines."}
        ],
        "correct_option_id": "B",
        "explanation": "The GIL prevents multiple threads from executing Python bytecodes in parallel in CPython. For CPU-bound tasks, multiprocessing must be used instead of multithreading to scale across cores.",
        "weight": 1
    },

    # NumPy
    {
        "id": "ds_numpy_001",
        "domain": "data_science",
        "skill": "NumPy",
        "difficulty": "easy",
        "question": "What is the term for NumPy applying arithmetic operations element-wise to arrays of different shapes during operations?",
        "options": [
            {"id": "A", "text": "Vectorization"},
            {"id": "B", "text": "Broadcasting"},
            {"id": "C", "text": "Reshaping"},
            {"id": "D", "text": "Slicing"}
        ],
        "correct_option_id": "B",
        "explanation": "Broadcasting describes how NumPy treats arrays with different shapes during arithmetic operations under certain constraints.",
        "weight": 1
    },
    {
        "id": "ds_numpy_002",
        "domain": "data_science",
        "skill": "NumPy",
        "difficulty": "medium",
        "question": "Why are NumPy array operations significantly faster than standard Python list loops for mathematical tasks?",
        "options": [
            {"id": "A", "text": "NumPy automatically compiles code to CUDA on the fly."},
            {"id": "B", "text": "NumPy arrays are homogeneous, contiguous memory structures that utilize vectorized C-implemented loops, avoiding Python overhead and dynamic typing lookups."},
            {"id": "C", "text": "NumPy skips arithmetic operations that result in decimals."},
            {"id": "D", "text": "NumPy forces CPU cores to overclock automatically."}
        ],
        "correct_option_id": "B",
        "explanation": "NumPy ndarrays are dense blocks of homogeneous data stored contiguously, allowing C code to execute iterations directly without runtime type checking or pointer dereferencing common in Python lists.",
        "weight": 1
    },
    {
        "id": "ds_numpy_003",
        "domain": "data_science",
        "skill": "NumPy",
        "difficulty": "hard",
        "question": "You slice a NumPy array `b = a[1:5, 1:5]`. If you modify a value in `b`, what happens to `a`?",
        "options": [
            {"id": "A", "text": "Nothing, since slicing returns a deep copy of the array data."},
            {"id": "B", "text": "The corresponding value in `a` is modified because slicing returns a view sharing the same underlying memory buffer."},
            {"id": "C", "text": "NumPy raises a ReadOnlyError because views are immutable."},
            {"id": "D", "text": "A runtime warning is printed and the system defaults to generating a copy."}
        ],
        "correct_option_id": "B",
        "explanation": "In NumPy, slicing creates a 'view' rather than a copy. Modifying the view will mutate the original array. If you need a copy, you must explicitly call `b = a[1:5, 1:5].copy()`.",
        "weight": 1
    },

    # Pandas
    {
        "id": "ds_pandas_001",
        "domain": "data_science",
        "skill": "Pandas",
        "difficulty": "easy",
        "question": "Which Pandas DataFrame method is used to remove rows containing missing values (NaN)?",
        "options": [
            {"id": "A", "text": "drop_missing()"},
            {"id": "B", "text": "dropna()"},
            {"id": "C", "text": "fillna()"},
            {"id": "D", "text": "remove_null()"}
        ],
        "correct_option_id": "B",
        "explanation": "dropna() removes rows or columns containing null (NaN) values.",
        "weight": 1
    },
    {
        "id": "ds_pandas_002",
        "domain": "data_science",
        "skill": "Pandas",
        "difficulty": "medium",
        "question": "In Pandas, what is the conceptual difference between using `.loc` and `.iloc` for selecting data?",
        "options": [
            {"id": "A", "text": "loc is for labels, while iloc is for integer-based index positions."},
            {"id": "B", "text": "loc is for rows, and iloc is only for columns."},
            {"id": "C", "text": "iloc is faster because it works in-place, whereas loc makes a copy."},
            {"id": "D", "text": "There is no difference; they are aliases."}
        ],
        "correct_option_id": "A",
        "explanation": ".loc is label-based indexing (e.g. df.loc['row_label', 'col_label']), while .iloc is integer-position based indexing (e.g. df.iloc[0, 1]).",
        "weight": 1
    },
    {
        "id": "ds_pandas_003",
        "domain": "data_science",
        "skill": "Pandas",
        "difficulty": "hard",
        "question": "You are performing a grouping operation `df.groupby('A')['B'].transform('mean')`. What is the difference between this and `df.groupby('A')['B'].mean()`?",
        "options": [
            {"id": "A", "text": "mean() returns a Series with a length equal to the number of unique groups, while transform('mean') returns a Series with the same shape as the original DataFrame containing the mapped group means."},
            {"id": "B", "text": "transform() is slower because it converts values to string types first."},
            {"id": "C", "text": "mean() outputs values in sorted order, while transform() outputs values in random order."},
            {"id": "D", "text": "mean() aggregates rows, while transform() removes all grouping keys."}
        ],
        "correct_option_id": "A",
        "explanation": "`.mean()` computes aggregate stats returning group size shape. `.transform()` computes the group-level metrics but broadcasts them back to align with original row positions, outputting identical dimensions to the inputs.",
        "weight": 1
    },

    # Statistics
    {
        "id": "ds_stats_001",
        "domain": "data_science",
        "skill": "Statistics",
        "difficulty": "easy",
        "question": "Which statistical measure of central tendency is calculated by sum of all values divided by count?",
        "options": [
            {"id": "A", "text": "Median"},
            {"id": "B", "text": "Mean"},
            {"id": "C", "text": "Mode"},
            {"id": "D", "text": "Standard Deviation"}
        ],
        "correct_option_id": "B",
        "explanation": "The mean (arithmetic average) is the sum of observations divided by the number of observations.",
        "weight": 1
    },
    {
        "id": "ds_stats_002",
        "domain": "data_science",
        "skill": "Statistics",
        "difficulty": "medium",
        "question": "What is the standard interpretation of a p-value of 0.03 in a hypothesis test with a significance level (alpha) of 0.05?",
        "options": [
            {"id": "A", "text": "Fail to reject the null hypothesis; the result is not statistically significant."},
            {"id": "B", "text": "Reject the null hypothesis; the result is statistically significant."},
            {"id": "C", "text": "The null hypothesis has a 3% chance of being true."},
            {"id": "D", "text": "The alternative hypothesis has a 97% chance of being true."}
        ],
        "correct_option_id": "B",
        "explanation": "Since p-value (0.03) < alpha (0.05), we reject the null hypothesis in favor of the alternative hypothesis as the result is statistically significant.",
        "weight": 1
    },
    {
        "id": "ds_stats_003",
        "domain": "data_science",
        "skill": "Statistics",
        "difficulty": "hard",
        "question": "Explain the difference between covariance and correlation as measures of relationship between two variables.",
        "options": [
            {"id": "A", "text": "Covariance measures linear relationships, whereas correlation only measures non-linear relationships."},
            {"id": "B", "text": "Covariance indicates direction only and is scale-dependent, while correlation is scaled (normalized) between -1 and 1, indicating both direction and strength independently of scale."},
            {"id": "C", "text": "Covariance is calculated using variance, while correlation is calculated using median absolute deviation."},
            {"id": "D", "text": "Covariance is normalized between -1 and 1, whereas correlation is unbound."}
        ],
        "correct_option_id": "B",
        "explanation": "Covariance measures how variables move together but its units depend on the variable scales. Correlation is covariance normalized by standard deviations, yielding a dimensionless scale between -1 and 1.",
        "weight": 1
    },

    # Data Cleaning
    {
        "id": "ds_clean_001",
        "domain": "data_science",
        "skill": "Data Cleaning",
        "difficulty": "easy",
        "question": "What is the first step in handling duplicate rows in a Pandas DataFrame?",
        "options": [
            {"id": "A", "text": "Use `df.drop_duplicates()` to remove identical rows"},
            {"id": "B", "text": "Use `df.fillna()` with a zero value"},
            {"id": "C", "text": "Run `df.describe()` to plot values"},
            {"id": "D", "text": "Perform log transformation"}
        ],
        "correct_option_id": "A",
        "explanation": "`drop_duplicates()` identifies and drops rows where all (or specific) column values are identical.",
        "weight": 1
    },
    {
        "id": "ds_clean_002",
        "domain": "data_science",
        "skill": "Data Cleaning",
        "difficulty": "medium",
        "question": "When cleaning missing numerical data, why might imputing with the median be preferred over the mean?",
        "options": [
            {"id": "A", "text": "The median is computationally faster to compute on all datasets."},
            {"id": "B", "text": "The mean is highly sensitive to extreme outliers, which can skew the imputed value, while the median is robust to outliers."},
            {"id": "C", "text": "The median automatically scales the values between 0 and 1."},
            {"id": "D", "text": "Median imputation preserves categorical strings."}
        ],
        "correct_option_id": "B",
        "explanation": "Outliers bias the mean. If a dataset has high skewness (e.g. income levels), the mean will be pulled upward, making median the better measure of central tendency for imputation.",
        "weight": 1
    },
    {
        "id": "ds_clean_003",
        "domain": "data_science",
        "skill": "Data Cleaning",
        "difficulty": "hard",
        "question": "Describe the risk of treating missing values by simply dropping rows (listwise deletion) in a dataset where data is not Missing Completely at Random (MCAR).",
        "options": [
            {"id": "A", "text": "It has no impact since dropping rows only reduces sample size."},
            {"id": "B", "text": "It introduces systemic bias into the dataset because the missingness is correlated with other variables, leading to invalid inference and skewed model parameters."},
            {"id": "C", "text": "It causes the target variable to switch values between positive and negative."},
            {"id": "D", "text": "It makes SQL queries run significantly slower."}
        ],
        "correct_option_id": "B",
        "explanation": "If data is not MCAR (e.g., high-income individuals refusing to report income), dropping rows results in non-random loss of information. The remaining subset is biased (e.g., under-representing high incomes), invalidating modeling outcomes.",
        "weight": 1
    },

    # Exploratory Data Analysis
    {
        "id": "ds_eda_001",
        "domain": "data_science",
        "skill": "Exploratory Data Analysis",
        "difficulty": "easy",
        "question": "Which visualization is best suited for showing the distribution of a single continuous variable?",
        "options": [
            {"id": "A", "text": "Scatter plot"},
            {"id": "B", "text": "Pie chart"},
            {"id": "C", "text": "Histogram"},
            {"id": "D", "text": "Line chart"}
        ],
        "correct_option_id": "C",
        "explanation": "A histogram groups continuous values into bins, counting occurrences in each bin to visualize distribution shapes.",
        "weight": 1
    },
    {
        "id": "ds_eda_002",
        "domain": "data_science",
        "skill": "Exploratory Data Analysis",
        "difficulty": "medium",
        "question": "In a box plot, what statistical values represent the box boundaries and the whiskers?",
        "options": [
            {"id": "A", "text": "Boundaries are the minimum and maximum; whiskers are the standard deviations."},
            {"id": "B", "text": "Boundaries represent the 25th percentile (Q1) and 75th percentile (Q3), while whiskers represent values within 1.5 times the Interquartile Range (IQR) from the quartiles."},
            {"id": "C", "text": "Boundaries are the mean and standard error; whiskers are standard deviations."},
            {"id": "D", "text": "Boundaries represent class probabilities; whiskers represent regression limits."}
        ],
        "correct_option_id": "B",
        "explanation": "A box plot visualizes Q1, Q2 (median), Q3. The IQR is (Q3 - Q1). Whiskers extend to the furthest points within 1.5 * IQR. Points beyond this are plotted as individual outliers.",
        "weight": 1
    },
    {
        "id": "ds_eda_003",
        "domain": "data_science",
        "skill": "Exploratory Data Analysis",
        "difficulty": "hard",
        "question": "You compute a Pearson correlation coefficient matrix and find a high correlation (r = 0.85) between features X and Y. What should you evaluate before drawing conclusions?",
        "options": [
            {"id": "A", "text": "Ensure that the relationship is strictly linear, check for influential outliers using a scatter plot, and verify if X and Y share a common confounding variable."},
            {"id": "B", "text": "Verify if the values of X and Y sum to exactly 1."},
            {"id": "C", "text": "Run an ANOVA test to confirm that both means are identical."},
            {"id": "D", "text": "Remove the column with the lower standard deviation immediately."}
        ],
        "correct_option_id": "A",
        "explanation": "Pearson correlation measures linear relationships. Outliers can heavily inflate/deflate Pearson's r. Furthermore, correlation does not imply causation; a third variable (confounder) could drive both, requiring visual validation (scatter plot) and domain logic review.",
        "weight": 1
    },

    # Data Visualization
    {
        "id": "ds_viz_001",
        "domain": "data_science",
        "skill": "Data Visualization",
        "difficulty": "easy",
        "question": "Which Python library is standard for plotting graphs and is the low-level foundation for Seaborn?",
        "options": [
            {"id": "A", "text": "Pandas"},
            {"id": "B", "text": "Matplotlib"},
            {"id": "C", "text": "Scikit-Learn"},
            {"id": "D", "text": "Numpy"}
        ],
        "correct_option_id": "B",
        "explanation": "Matplotlib is the core plotting library in Python's data ecosystem, and Seaborn wraps it to provide high-level abstractions.",
        "weight": 1
    },
    {
        "id": "ds_viz_002",
        "domain": "data_science",
        "skill": "Data Visualization",
        "difficulty": "medium",
        "question": "For visualizing trends over a continuous variable (like timeline sales over months), which plot is most appropriate?",
        "options": [
            {"id": "A", "text": "Bar chart"},
            {"id": "B", "text": "Line chart"},
            {"id": "C", "text": "Scatter plot"},
            {"id": "D", "text": "Box plot"}
        ],
        "correct_option_id": "B",
        "explanation": "Line charts connect data points sequentially, making them optimal for displaying time-series trends and sequential developments.",
        "weight": 1
    },
    {
        "id": "ds_viz_003",
        "domain": "data_science",
        "skill": "Data Visualization",
        "difficulty": "hard",
        "question": "When designing dashboards, how does the choice of chart type differ when displaying composition over time versus a single snapshot comparison?",
        "options": [
            {"id": "A", "text": "Use a pie chart for both scenarios to maintain consistent dashboard styles."},
            {"id": "B", "text": "Use stacked area charts or stacked bar charts for composition changes over time, and simple horizontal bar charts or treemaps for snapshot comparisons."},
            {"id": "C", "text": "Snapshot comparisons require line charts, while temporal composition requires scatter plots."},
            {"id": "D", "text": "Always convert temporal composition data to linear regressions before plotting."}
        ],
        "correct_option_id": "B",
        "explanation": "Stacked area/bar charts show relative breakdowns as they change sequentially over time. Snapshot comparisons are best served by simple bar charts or treemaps because pie charts over time become hard to read.",
        "weight": 1
    },

    # SQL
    {
        "id": "ds_sql_001",
        "domain": "data_science",
        "skill": "SQL",
        "difficulty": "easy",
        "question": "Which SQL clause is used to filter query results based on conditions?",
        "options": [
            {"id": "A", "text": "GROUP BY"},
            {"id": "B", "text": "WHERE"},
            {"id": "C", "text": "ORDER BY"},
            {"id": "D", "text": "SELECT"}
        ],
        "correct_option_id": "B",
        "explanation": "The WHERE clause filters rows returned by the FROM clause based on boolean search conditions.",
        "weight": 1
    },
    {
        "id": "ds_sql_002",
        "domain": "data_science",
        "skill": "SQL",
        "difficulty": "medium",
        "question": "In SQL, what is the difference between WHERE and HAVING clauses?",
        "options": [
            {"id": "A", "text": "WHERE is for filtering individual rows, while HAVING is for filtering aggregated group rows calculated after GROUP BY."},
            {"id": "B", "text": "WHERE can only be used on string columns, while HAVING only works on numbers."},
            {"id": "C", "text": "HAVING runs before the JOIN operations, whereas WHERE runs after JOINs."},
            {"id": "D", "text": "There is no difference; they can be used interchangeably."}
        ],
        "correct_option_id": "A",
        "explanation": "WHERE filters source rows before grouping. HAVING filters the grouped results using aggregate functions (e.g. `HAVING COUNT(*) > 5`).",
        "weight": 1
    },
    {
        "id": "ds_sql_003",
        "domain": "data_science",
        "skill": "SQL",
        "difficulty": "hard",
        "question": "Explain the difference in execution behavior and output between LEFT JOIN, INNER JOIN, and FULL OUTER JOIN.",
        "options": [
            {"id": "A", "text": "INNER JOIN retains all rows; LEFT JOIN drops all columns; FULL JOIN matches rows horizontally."},
            {"id": "B", "text": "INNER JOIN returns only matching rows; LEFT JOIN returns all rows from the left table and matching rows from the right (filling right columns with NULL for mismatches); FULL OUTER JOIN returns all rows from both tables, filling mismatches with NULLs."},
            {"id": "C", "text": "LEFT JOIN only matches rows if they are sorted; INNER JOIN executes faster because it skips indexes."},
            {"id": "D", "text": "LEFT JOIN drops matching rows, and FULL OUTER JOIN matches rows on primary keys only."}
        ],
        "correct_option_id": "B",
        "explanation": "INNER JOIN restricts the result to intersecting rows. LEFT JOIN preserves all rows from the left table, injecting NULLs for right-table missing elements. FULL OUTER JOIN preserves all rows from both tables, with NULL values where rows do not align on join keys.",
        "weight": 1
    },

    # Machine Learning Basics
    {
        "id": "ds_mlbas_001",
        "domain": "data_science",
        "skill": "Machine Learning Basics",
        "difficulty": "easy",
        "question": "Which machine learning paradigm involves training models on labeled inputs to predict known outcomes?",
        "options": [
            {"id": "A", "text": "Unsupervised Learning"},
            {"id": "B", "text": "Supervised Learning"},
            {"id": "C", "text": "Reinforcement Learning"},
            {"id": "D", "text": "Semi-supervised Clustering"}
        ],
        "correct_option_id": "B",
        "explanation": "Supervised learning learns mappings from input features to target labels, using labels as guidance (supervision).",
        "weight": 1
    },
    {
        "id": "ds_mlbas_002",
        "domain": "data_science",
        "skill": "Machine Learning Basics",
        "difficulty": "medium",
        "question": "What does a Decision Tree split on at each node during training?",
        "options": [
            {"id": "A", "text": "Random mathematical equations."},
            {"id": "B", "text": "The feature and split point that maximizes information gain (or minimizes Gini impurity/MSE)."},
            {"id": "C", "text": "An average of all feature vectors."},
            {"id": "D", "text": "Class distributions determined by an SVM kernel."}
        ],
        "correct_option_id": "B",
        "explanation": "Decision trees choose splits that maximize impurity reduction (Gini index or Information Gain for classification, variance reduction/MSE for regression).",
        "weight": 1
    },
    {
        "id": "ds_mlbas_003",
        "domain": "data_science",
        "skill": "Machine Learning Basics",
        "difficulty": "hard",
        "question": "What is the bias-variance tradeoff, and how do overfitting and underfitting relate to these concepts?",
        "options": [
            {"id": "A", "text": "Bias is testing error, and variance is validation error. Overfitting is high bias; underfitting is low variance."},
            {"id": "B", "text": "Underfitting is caused by high bias (simple model assumptions fail to capture patterns), while overfitting is caused by high variance (model fits training data/noise too closely, failing to generalize)."},
            {"id": "C", "text": "Bias measures predictions accuracy, while variance measures training speeds. Overfitting is when models are too slow."},
            {"id": "D", "text": "Underfitting is high variance; overfitting is low bias."}
        ],
        "correct_option_id": "B",
        "explanation": "Bias represents model assumptions errors. High bias models underfit (too simple). Variance is sensitivity to training fluctuations. High variance models overfit (capture noise), leading to poor test generalization.",
        "weight": 1
    },

    # Data Interpretation
    {
        "id": "ds_interpret_001",
        "domain": "data_science",
        "skill": "Data Interpretation",
        "difficulty": "easy",
        "question": "What is the primary fallacy in concluding that ice cream sales cause drownings because both peak during the summer?",
        "options": [
            {"id": "A", "text": "Correlation does not imply causation (omitted variable bias)"},
            {"id": "B", "text": "Sample size is too small"},
            {"id": "C", "text": "Ice cream actually has a biological link to swimming cramps"},
            {"id": "D", "text": "The data is improperly scaled"}
        ],
        "correct_option_id": "A",
        "explanation": "The relationship is a correlation driven by a confounding variable (hot weather), meaning one does not cause the other.",
        "weight": 1
    },
    {
        "id": "ds_interpret_002",
        "domain": "data_science",
        "skill": "Data Interpretation",
        "difficulty": "medium",
        "question": "Explain Simpson's Paradox in statistical analysis.",
        "options": [
            {"id": "A", "text": "It states that smaller samples have larger variances."},
            {"id": "B", "text": "A trend that appears in different groups of data disappears or reverses when these groups are combined."},
            {"id": "C", "text": "It means all correlation coefficients approach zero in massive datasets."},
            {"id": "D", "text": "It is when outlier values represent correct labels."}
        ],
        "correct_option_id": "B",
        "explanation": "Simpson's Paradox occurs when aggregate statistics hide or invert relationships present in sub-categories due to confounding factors.",
        "weight": 1
    },
    {
        "id": "ds_interpret_003",
        "domain": "data_science",
        "skill": "Data Interpretation",
        "difficulty": "hard",
        "question": "An analytics dashboard claims a feature change increased conversion rate from 1.0% to 1.1% based on 1,000 visitors in an A/B test. How should you interpret this result?",
        "options": [
            {"id": "A", "text": "Celebrate the 10% increase because conversion improved."},
            {"id": "B", "text": "Run a statistical significance test (e.g. chi-squared or z-test); at 1,000 visitors, the change from 1.0% to 1.1% is highly likely to be statistically insignificant noise."},
            {"id": "C", "text": "Conclude that the sample size is double what is needed for a reliable test."},
            {"id": "D", "text": "Double the conversion metric scale on the visual axis to emphasize the change."}
        ],
        "correct_option_id": "B",
        "explanation": "For tiny changes (0.1% absolute lift), small sample sizes (1,000 visitors total) yield low statistical power, making the margin of error much larger than the detected lift. A z-test or chi-squared test would confirm the difference is insignificant noise.",
        "weight": 1
    }
]

# 3. GENERATIVE AI QUESTIONS
genai_questions = [
    # LLM Fundamentals
    {
        "id": "genai_llm_001",
        "domain": "generative_ai",
        "skill": "LLM Fundamentals",
        "difficulty": "easy",
        "question": "What is the primary loss objective used when pre-training autoregressive LLMs (like GPT)?",
        "options": [
            {"id": "A", "text": "Contrastive Loss"},
            {"id": "B", "text": "Causal Language Modeling (predicting the next token)"},
            {"id": "C", "text": "Mean Squared Error on word positions"},
            {"id": "D", "text": "Sequence-to-Sequence Translation mapping"}
        ],
        "correct_option_id": "B",
        "explanation": "Autoregressive models are trained using Causal Language Modeling (CLM) where the model predicts the next token given preceding context.",
        "weight": 1
    },
    {
        "id": "genai_llm_002",
        "domain": "generative_ai",
        "skill": "LLM Fundamentals",
        "difficulty": "medium",
        "question": "In LLM generation, what is the impact of setting the temperature parameter close to 0?",
        "options": [
            {"id": "A", "text": "The model's output becomes highly deterministic, repeatedly picking the most probable tokens."},
            {"id": "B", "text": "The model stops processing inputs due to execution timeout."},
            {"id": "C", "text": "The output becomes highly creative and randomized."},
            {"id": "D", "text": "It increases the length of the generated tokens."}
        ],
        "correct_option_id": "A",
        "explanation": "Temperature controls the scaling of logits before softmax. Lower temperature (approaching 0) sharpens the probability distribution, forcing the model to select top tokens (making output deterministic).",
        "weight": 1
    },
    {
        "id": "genai_llm_003",
        "domain": "generative_ai",
        "skill": "LLM Fundamentals",
        "difficulty": "hard",
        "question": "Describe the mechanistic differences between RLHF (PPO) and DPO (Direct Preference Optimization) for aligning LLMs.",
        "options": [
            {"id": "A", "text": "RLHF uses contrastive learning, while DPO trains an auxiliary actor-critic model."},
            {"id": "B", "text": "RLHF requires training a separate reward model and runs computationally expensive reinforcement learning (PPO); DPO mathematically bypasses the reward model, optimizing the policy directly using preference binary cross-entropy."},
            {"id": "C", "text": "DPO requires vector databases, while RLHF runs strictly in memory loops."},
            {"id": "D", "text": "DPO relies on prompt engineering, whereas RLHF edits model weights directly."}
        ],
        "correct_option_id": "B",
        "explanation": "RLHF requires building a reward model followed by PPO actor-critic optimization loops (unstable and memory-heavy). DPO derives closed-form equations showing preference loss directly correlates to token probabilities, training the policy on labeled binary preferences directly.",
        "weight": 1
    },

    # Prompt Engineering
    {
        "id": "genai_prompt_001",
        "domain": "generative_ai",
        "skill": "Prompt Engineering",
        "difficulty": "easy",
        "question": "Which prompt engineering technique involves showing the model a few input-output examples before the target query?",
        "options": [
            {"id": "A", "text": "Zero-shot prompting"},
            {"id": "B", "text": "Few-shot prompting"},
            {"id": "C", "text": "Meta-prompting"},
            {"id": "D", "text": "Chain of Thought"}
        ],
        "correct_option_id": "B",
        "explanation": "Few-shot prompting provides in-context examples to help the model identify context patterns and format target requirements.",
        "weight": 1
    },
    {
        "id": "genai_prompt_002",
        "domain": "generative_ai",
        "skill": "Prompt Engineering",
        "difficulty": "medium",
        "question": "What is the key mechanism of Chain of Thought (CoT) prompting, and why does it improve LLM reasoning?",
        "options": [
            {"id": "A", "text": "It forces the model to generate multiple answers in parallel and take a majority vote."},
            {"id": "B", "text": "It prompts the model to generate its intermediate logical reasoning steps before outputting the final answer, allocating more compute tokens to logical derivation."},
            {"id": "C", "text": "It shortens prompts to prevent context window overflow."},
            {"id": "D", "text": "It encrypts the prompt text to bypass safety filters."}
        ],
        "correct_option_id": "B",
        "explanation": "CoT prompts the model to output step-by-step reasoning. Because transformers process sequentially, generating reasoning tokens allows the model to compute intermediate logic, improving complex problem solving.",
        "weight": 1
    },
    {
        "id": "genai_prompt_003",
        "domain": "generative_ai",
        "skill": "Prompt Engineering",
        "difficulty": "hard",
        "question": "Explain the structure and utility of ReAct (Reasoning and Acting) prompting pattern for agentic workflows.",
        "options": [
            {"id": "A", "text": "It compiles prompts into Javascript React components to render web interfaces."},
            {"id": "B", "text": "It structures prompts into alternating cycles of Thought (reasoning), Action (calling external tools), and Observation (receiving tool output) to solve problems dynamically."},
            {"id": "C", "text": "It is a fine-tuning loss function that penalizes long outputs."},
            {"id": "D", "text": "It limits prompt syntax strictly to XML schemas."}
        ],
        "correct_option_id": "B",
        "explanation": "ReAct combines reasoning and acting. By alternating Thought (LLM analyzes situation), Action (LLM selects tool/inputs), and Observation (system feeds back tool response), the LLM dynamically interacts with external APIs to accomplish goals.",
        "weight": 1
    },

    # Tokens & Context Windows
    {
        "id": "genai_tokens_001",
        "domain": "generative_ai",
        "skill": "Tokens & Context Windows",
        "difficulty": "easy",
        "question": "What is a 'token' in the context of LLMs?",
        "options": [
            {"id": "A", "text": "A secure API key used for billing"},
            {"id": "B", "text": "Sub-word segments or characters representing the basic units of text processed by the model"},
            {"id": "C", "text": "A vector stored in a vector database"},
            {"id": "D", "text": "The weight matrix inside transformer feedforward layers"}
        ],
        "correct_option_id": "B",
        "explanation": "Tokenizers split raw text into integer-mapped sub-word tokens, representing the basic numerical inputs/outputs of LLMs.",
        "weight": 1
    },
    {
        "id": "genai_tokens_002",
        "domain": "generative_ai",
        "skill": "Tokens & Context Windows",
        "difficulty": "medium",
        "question": "What is 'needle in a haystack' (NIAH) testing in context window evaluation?",
        "options": [
            {"id": "A", "text": "Evaluating if a tokenizer can identify hidden punctuation marks."},
            {"id": "B", "text": "Retrieving a specific small piece of information (needle) placed at various positions within a massive context block (haystack) to evaluate recall accuracy."},
            {"id": "C", "text": "Compressing LLM parameters using integer quantization."},
            {"id": "D", "text": "Evaluating if an agent can write Python code without bugs."}
        ],
        "correct_option_id": "B",
        "explanation": "NIAH evaluates context utilization. It inserts a random fact at different depth percentiles in long documents to verify if the LLM's attention mechanism can retrieve it correctly.",
        "weight": 1
    },
    {
        "id": "genai_tokens_003",
        "domain": "generative_ai",
        "skill": "Tokens & Context Windows",
        "difficulty": "hard",
        "question": "How does FlashAttention optimize the standard Self-Attention calculation to permit long context windows?",
        "options": [
            {"id": "A", "text": "It drops standard QKV projections, replacing them with linear regressions."},
            {"id": "B", "text": "It computes attention in-memory by tiling blocks, minimizing read/write operations between GPU HBM (High Bandwidth Memory) and SRAM, yielding O(N) memory IO savings."},
            {"id": "C", "text": "It converts token IDs to 4-bit integers on the fly during training loops."},
            {"id": "D", "text": "It distributes calculations across remote REST APIs to save local resources."}
        ],
        "correct_option_id": "B",
        "explanation": "Standard attention is bounded by memory reads/writes. FlashAttention tiles attention matrix blocks into fast GPU SRAM, avoiding writing the intermediate NxN attention matrix to slow HBM, accelerating execution speeds.",
        "weight": 1
    },

    # Embeddings
    {
        "id": "genai_embed_001",
        "domain": "generative_ai",
        "skill": "Embeddings",
        "difficulty": "easy",
        "question": "What is the primary purpose of embeddings in an NLP system?",
        "options": [
            {"id": "A", "text": "Represent information as numerical vectors in a continuous vector space"},
            {"id": "B", "text": "Encrypt user input data before database storage"},
            {"id": "C", "text": "Increase network bandwidth speeds"},
            {"id": "D", "text": "Compile Python code into machine code"}
        ],
        "correct_option_id": "A",
        "explanation": "Embeddings represent semantic information using numerical vectors.",
        "weight": 1
    },
    {
        "id": "genai_embed_002",
        "domain": "generative_ai",
        "skill": "Embeddings",
        "difficulty": "medium",
        "question": "Why is Cosine Similarity generally preferred over Euclidean Distance for evaluating similarity between text embeddings?",
        "options": [
            {"id": "A", "text": "Cosine similarity measures vector magnitudes, which represents token length differences."},
            {"id": "B", "text": "Cosine similarity evaluates the angle between vectors, normalizing for document/token length differences, whereas Euclidean distance is sensitive to vector magnitudes."},
            {"id": "C", "text": "Euclidean distance is only mathematically valid in two-dimensional coordinate systems."},
            {"id": "D", "text": "Cosine similarity runs in constant time O(1) regardless of dimensions."}
        ],
        "correct_option_id": "B",
        "explanation": "Cosine similarity measures the angular similarity. In text embeddings, longer texts can have higher vector magnitudes (Euclidean distance is large), but they share the same direction (cosine similarity is close to 1).",
        "weight": 1
    },
    {
        "id": "genai_embed_003",
        "domain": "generative_ai",
        "skill": "Embeddings",
        "difficulty": "hard",
        "question": "You are building a multilingual semantic search engine. You notice search queries in French fail to return matching English documents despite using a vector search setup. What is the root cause?",
        "options": [
            {"id": "A", "text": "The vector database does not support UTF-8 encoded search inputs."},
            {"id": "B", "text": "You are using a monolingual English embedding model, which maps French inputs to unrelated vector spaces. You must switch to a joint multilingual embedding model."},
            {"id": "C", "text": "The cosine similarity formula needs to be modified for foreign languages."},
            {"id": "D", "text": "English and French embeddings have different dimensionality configurations by definition."}
        ],
        "correct_option_id": "B",
        "explanation": "Monolingual models map different languages to distinct regions of vector space. A multilingual model (e.g. Cohere Multilingual, mUSE) is trained on translation pairs to map semantically equivalent sentences to overlapping vector spaces.",
        "weight": 1
    },

    # Vector Databases
    {
        "id": "genai_vectordb_001",
        "domain": "generative_ai",
        "skill": "Vector Databases",
        "difficulty": "easy",
        "question": "What is the primary role of a Vector Database in a RAG system?",
        "options": [
            {"id": "A", "text": "To execute SQL join queries on user accounts"},
            {"id": "B", "text": "To store and search high-dimensional embeddings efficiently using similarity metrics"},
            {"id": "C", "text": "To compile fine-tuned weights of transformers"},
            {"id": "D", "text": "To convert PDF text to markdown formats"}
        ],
        "correct_option_id": "B",
        "explanation": "Vector databases index embeddings (vectors) to support fast approximate nearest neighbor (ANN) lookups.",
        "weight": 1
    },
    {
        "id": "genai_vectordb_002",
        "domain": "generative_ai",
        "skill": "Vector Databases",
        "difficulty": "medium",
        "question": "How does HNSW (Hierarchical Navigable Small World) index optimize vector search speeds compared to a flat index?",
        "options": [
            {"id": "A", "text": "It uses standard binary trees, which guarantees O(log N) search times."},
            {"id": "B", "text": "It constructs a multi-layer graph where top layers have sparse connections for fast routing, and lower layers have dense connections for precise search, avoiding scanning every database vector (flat scan)."},
            {"id": "C", "text": "It maps vectors into hash tables to achieve O(1) query times."},
            {"id": "D", "text": "It converts float vectors into integer indexes, sacrificing all precision."}
        ],
        "correct_option_id": "B",
        "explanation": "HNSW builds hierarchical graphs. Search starts at top layers (skip list structure) to traverse large distances fast, dropping down to lower layers for localized proximity clustering, drastically speeding up queries.",
        "weight": 1
    },
    {
        "id": "genai_vectordb_003",
        "domain": "generative_ai",
        "skill": "Vector Databases",
        "difficulty": "hard",
        "question": "Describe the tradeoff between Product Quantization (PQ) and Flat indexing in a vector database containing 100 million vectors.",
        "options": [
            {"id": "A", "text": "PQ speeds up search times but requires rebuilding the entire database on every insert."},
            {"id": "B", "text": "PQ compresses high-dimensional vectors to smaller byte codes, significantly reducing memory footprint and accelerating search speeds, but introduces quantization errors that reduce search recall precision compared to Flat indexing."},
            {"id": "C", "text": "Flat indexing requires less RAM but is slower, while PQ requires more RAM but is faster."},
            {"id": "D", "text": "There is no difference; both index types use identical memory and search latency properties."}
        ],
        "correct_option_id": "B",
        "explanation": "PQ splits vectors into sub-vectors and quantizes them into centroids, saving up to 95% RAM and increasing speeds, but since it is lossy compression, the similarity calculations are approximations, yielding lower recall.",
        "weight": 1
    },

    # RAG
    {
        "id": "genai_rag_001",
        "domain": "generative_ai",
        "skill": "RAG",
        "difficulty": "easy",
        "question": "What does the abbreviation RAG stand for in generative AI system design?",
        "options": [
            {"id": "A", "text": "Random Access Generation"},
            {"id": "B", "text": "Retrieval-Augmented Generation"},
            {"id": "C", "text": "Recurrent Attention Gradients"},
            {"id": "D", "text": "Reinforced Action Graphs"}
        ],
        "correct_option_id": "B",
        "explanation": "RAG combines search retrieval methods with generative models to output factually correct answers using external documents.",
        "weight": 1
    },
    {
        "id": "genai_rag_002",
        "domain": "generative_ai",
        "skill": "RAG",
        "difficulty": "medium",
        "question": "What is the primary role of a Re-ranker model (e.g. Cohere Rerank) in a multi-stage RAG pipeline?",
        "options": [
            {"id": "A", "text": "It converts retrieved vectors back into markdown documents."},
            {"id": "B", "text": "It takes the initial retrieval candidate list (e.g. top 50) and uses a cross-encoder model to re-evaluate semantic relevance, outputting a high-precision subset (e.g. top 5) for the LLM prompt."},
            {"id": "C", "text": "It translates queries into different languages before indexing."},
            {"id": "D", "text": "It acts as a backup caching mechanism."}
        ],
        "correct_option_id": "B",
        "explanation": "Initial vector retrieval is fast but can miss deep relationships. A cross-encoder re-ranker processes query-document pairs jointly, recalculating highly accurate relevance scores to filter down candidates, reducing prompt clutter.",
        "weight": 1
    },
    {
        "id": "genai_rag_003",
        "domain": "generative_ai",
        "skill": "RAG",
        "difficulty": "hard",
        "question": "A RAG pipeline is returning relevant context, but the LLM still hallucinates answers or includes incorrect facts in its response. Which configuration change will mitigate this best?",
        "options": [
            {"id": "A", "text": "Increase the LLM's temperature parameter to 1.5 to encourage wider outputs."},
            {"id": "B", "text": "Apply system instructions enforcing strict alignment to the provided context, reduce the temperature parameter to 0, and use a re-ranking model to ensure only highly relevant context chunks are in the prompt."},
            {"id": "C", "text": "Switch to an embedding model with smaller dimensionality sizes."},
            {"id": "D", "text": "Increase the chunk size overlap limit to maximum context bounds."}
        ],
        "correct_option_id": "B",
        "explanation": "Hallucinations are minimized by restricting generation freedom (temp=0) and using strict system prompt templates (e.g., 'Answer ONLY using the provided text. If unknown, state I do not know.'). Re-ranking ensures clean context blocks.",
        "weight": 1
    },

    # Fine-tuning
    {
        "id": "genai_finetune_001",
        "domain": "generative_ai",
        "skill": "Fine-tuning",
        "difficulty": "easy",
        "question": "Which parameter-efficient fine-tuning (PEFT) technique injects low-rank decomposition matrices into transformer layers to reduce trainable weights?",
        "options": [
            {"id": "A", "text": "Prefix Tuning"},
            {"id": "B", "text": "LoRA (Low-Rank Adaptation)"},
            {"id": "C", "text": "Adapter Layers"},
            {"id": "D", "text": "Quantization"}
        ],
        "correct_option_id": "B",
        "explanation": "LoRA freezes base model weights and inserts small trainable low-rank matrices into attention layers, cutting trainable parameters drastically.",
        "weight": 1
    },
    {
        "id": "genai_finetune_002",
        "domain": "generative_ai",
        "skill": "Fine-tuning",
        "difficulty": "medium",
        "question": "In QLoRA, what is the primary memory-saving mechanism compared to standard LoRA?",
        "options": [
            {"id": "A", "text": "It drops all attention layer calculations completely."},
            {"id": "B", "text": "It quantizes the frozen base model parameters to a specialized 4-bit NormalFloat (NF4) data type and uses double quantization for scaling factors."},
            {"id": "C", "text": "It distributes calculations to external APIs during training loops."},
            {"id": "D", "text": "It removes backpropagation entirely, updating weights randomly."}
        ],
        "correct_option_id": "B",
        "explanation": "QLoRA combines quantization and LoRA. The base model weights are loaded in 4-bit NF4 representation, saving massive VRAM, and gradients are backpropagated through these frozen weights into active 16-bit LoRA adapters.",
        "weight": 1
    },
    {
        "id": "genai_finetune_003",
        "domain": "generative_ai",
        "skill": "Fine-tuning",
        "difficulty": "hard",
        "question": "You want an LLM to consistently generate structured outputs (e.g. JSON schemas matching strict database fields) and answer queries based on custom enterprise manuals. What is the optimal architecture choice?",
        "options": [
            {"id": "A", "text": "Fine-tune the model to learn the custom manuals, and use zero-shot prompts for the JSON output structure."},
            {"id": "B", "text": "Implement a RAG pipeline to retrieve updated manuals context dynamically, and use a structured parsing library (e.g., Instructor or Pydantic JSON validation) during inference to guarantee JSON compliance."},
            {"id": "C", "text": "Fine-tune the model on both documents and schemas; this guarantees 100% database schema compliance without any runtime code validations."},
            {"id": "D", "text": "Increase context windows to maximum sizes and append raw PDF strings."}
        ],
        "correct_option_id": "B",
        "explanation": "Fine-tuning is poor at learning specific facts or ensuring strict JSON structures (no reliability guarantees). RAG resolves fact retrieval dynamically. JSON compliance is strictly enforced at the API client level using parser constraints.",
        "weight": 1
    },

    # Transformers
    {
        "id": "genai_trans_001",
        "domain": "generative_ai",
        "skill": "Transformers",
        "difficulty": "easy",
        "question": "Which core mechanism introduced in the seminal 'Attention Is All You Need' paper allows transformers to process words in parallel?",
        "options": [
            {"id": "A", "text": "Recurrence loops"},
            {"id": "B", "text": "Self-Attention mechanism"},
            {"id": "C", "text": "Convolutions"},
            {"id": "D", "text": "Stochastic Gradient Descent"}
        ],
        "correct_option_id": "B",
        "explanation": "Self-attention computes relations between all words in a sequence simultaneously, bypassing the sequential bottlenecks of RNNs/LSTMs.",
        "weight": 1
    },
    {
        "id": "genai_trans_002",
        "domain": "generative_ai",
        "skill": "Transformers",
        "difficulty": "medium",
        "question": "In a transformer block, what is the role of Layer Normalization (LayerNorm)?",
        "options": [
            {"id": "A", "text": "It scales logits to sum to exactly 1."},
            {"id": "B", "text": "It stabilizes training by normalizing activations across features within a layer, preventing gradient explosion or vanishing."},
            {"id": "C", "text": "It compresses the weights of feedforward layers."},
            {"id": "D", "text": "It translates words into integer tokens."}
        ],
        "correct_option_id": "B",
        "explanation": "LayerNorm calculates mean and variance across the hidden dimensions of each single sample, stabilizing optimization processes and accelerating training convergence.",
        "weight": 1
    },
    {
        "id": "genai_trans_003",
        "domain": "generative_ai",
        "skill": "Transformers",
        "difficulty": "hard",
        "question": "Explain the difference in attention mask application between Encoder-only (e.g. BERT) and Decoder-only (e.g. GPT) transformer architectures.",
        "options": [
            {"id": "A", "text": "BERT uses bidirectional attention masking, whereas GPT uses causal masking to prevent tokens from attending to future tokens in the sequence."},
            {"id": "B", "text": "BERT masking forces sequential tokens, while GPT allows fully parallel attention projections."},
            {"id": "C", "text": "GPT uses zero-masked softmax, while BERT drops the softmax scaling factor."},
            {"id": "D", "text": "Encoder architectures cannot utilize masks by design."}
        ],
        "correct_option_id": "A",
        "explanation": "BERT is bidirectional (tokens attend to both left and right context). GPT is autoregressive and employs a lower-triangular causal attention mask, ensuring predictions for index i only depend on tokens up to index i-1.",
        "weight": 1
    },

    # AI Agents
    {
        "id": "genai_agents_001",
        "domain": "generative_ai",
        "skill": "AI Agents",
        "difficulty": "easy",
        "question": "What is the defining capability of an AI Agent compared to a simple LLM chatbot?",
        "options": [
            {"id": "A", "text": "It can run on mobile devices without internet connection."},
            {"id": "B", "text": "It can plan, call external tools/APIs, and make autonomous decisions based on observations to achieve a goal."},
            {"id": "C", "text": "It can store infinitely long conversations in its model parameters."},
            {"id": "D", "text": "It is written in binary C++ rather than Python script."}
        ],
        "correct_option_id": "B",
        "explanation": "Agents are action-oriented. They combine LLM generation with execution loops (planning, tool use, feedback reflection) to perform workflows autonomously.",
        "weight": 1
    },
    {
        "id": "genai_agents_002",
        "domain": "generative_ai",
        "skill": "AI Agents",
        "difficulty": "medium",
        "question": "What is the primary risk of using loops in multi-agent collaboration (e.g. CrewAI or AutoGen) and how is it typically handled?",
        "options": [
            {"id": "A", "text": "Agents will consume infinite tokens and enter infinite loops if they fail to converge on a solution; handled by implementing maximum iteration caps."},
            {"id": "B", "text": "Agents will overwrite database structures; handled by disabling SQL execution."},
            {"id": "C", "text": "It causes models to compile weights; handled by resetting cache files."},
            {"id": "D", "text": "It leads to syntax errors in tokenizers; handled by rewriting prompts."}
        ],
        "correct_option_id": "A",
        "explanation": "In multi-agent loops, agents can pass the same error back and forth (infinite critique cycles), incurring massive costs. Hard limits (max_iterations, timeouts, human-in-the-loop checks) prevent this.",
        "weight": 1
    },
    {
        "id": "genai_agents_003",
        "domain": "generative_ai",
        "skill": "AI Agents",
        "difficulty": "hard",
        "question": "Explain the concept of 'reflexion' (self-reflection) in agentic architectures and how it reduces execution failures.",
        "options": [
            {"id": "A", "text": "It is when the LLM mirrors the user's personality traits to build rapport."},
            {"id": "B", "text": "It evaluates agent outputs using a separate validation agent that generates text-based critiques of failures, which are appended to the agent's context window to guide subsequent attempts."},
            {"id": "C", "text": "It compiles code directly to assembly to trace variable allocation errors."},
            {"id": "D", "text": "It requires the agent to write unit tests before executing any tool."}
        ],
        "correct_option_id": "B",
        "explanation": "Reflexion is a meta-cognitive pattern. Rather than stopping on tool errors, the agent evaluates its execution trace, generates a critique of what went wrong, and feeds this back as prompt memory, leading to self-correction.",
        "weight": 1
    },

    # LLM Evaluation
    {
        "id": "genai_eval_001",
        "domain": "generative_ai",
        "skill": "LLM Evaluation",
        "difficulty": "easy",
        "question": "Which benchmark is widely used to evaluate LLM performance on general knowledge multiple-choice questions across diverse subjects?",
        "options": [
            {"id": "A", "text": "GLUE"},
            {"id": "B", "text": "MMLU (Massive Multitask Language Understanding)"},
            {"id": "C", "text": "ImageNet"},
            {"id": "D", "text": "BLEU"}
        ],
        "correct_option_id": "B",
        "explanation": "MMLU evaluates LLMs across elementary mathematics, US history, computer science, law, and other academic subjects.",
        "weight": 1
    },
    {
        "id": "genai_eval_002",
        "domain": "generative_ai",
        "skill": "LLM Evaluation",
        "difficulty": "medium",
        "question": "What is the primary limitation of utilizing BLEU or ROUGE metrics to evaluate the output quality of a summarization LLM?",
        "options": [
            {"id": "A", "text": "They require GPU acceleration to execute metrics calculation."},
            {"id": "B", "text": "They rely on exact n-gram overlap between generated and reference summaries, penalizing correct summaries that use different wording (synonyms)."},
            {"id": "C", "text": "They only support classification targets, not generated texts."},
            {"id": "D", "text": "They are bounded by context window size limits."}
        ],
        "correct_option_id": "B",
        "explanation": "BLEU/ROUGE are syntactic overlap metrics. They fail to evaluate semantic meaning. If the LLM generates a paraphrase using synonyms, overlap score drops, making them poor indicators of generation quality.",
        "weight": 1
    },
    {
        "id": "genai_eval_003",
        "domain": "generative_ai",
        "skill": "LLM Evaluation",
        "difficulty": "hard",
        "question": "You are implementing 'LLM-as-a-Judge' to evaluate agent dialogues. What biases must you monitor, and how do you reduce them?",
        "options": [
            {"id": "A", "text": "Token limits bias; resolved by truncating context lines."},
            {"id": "B", "text": "Self-favoritism bias (preferring own model output), position bias (ordering of options), and verbosity bias (preferring longer outputs); reduced by swap-testing response ordering, using high-quality rubric formatting, and setting sentence length constraints."},
            {"id": "C", "text": "SQL injection bias; resolved by sanitizing eval logs."},
            {"id": "D", "text": "There are no documented biases when utilizing GPT-4 as a judge."}
        ],
        "correct_option_id": "B",
        "explanation": "LLM judges exhibit position bias, length bias, and model familiarity bias. Mitigation involves swapping target candidate order in prompts, using chain of thought justification templates (rubrics), and length normalization constraints.",
        "weight": 1
    }
]

# 4. WEB DEVELOPMENT QUESTIONS
web_questions = [
    # HTML
    {
        "id": "web_html_001",
        "domain": "web_development",
        "skill": "HTML",
        "difficulty": "easy",
        "question": "Which HTML5 semantic tag represents an independent, self-contained piece of content (e.g. blog post)?",
        "options": [
            {"id": "A", "text": "<section>"},
            {"id": "B", "text": "<article>"},
            {"id": "C", "text": "<div>"},
            {"id": "D", "text": "<aside>"}
        ],
        "correct_option_id": "B",
        "explanation": "The <article> tag specifies independent, self-contained content that should be reusable and distributable.",
        "weight": 1
    },
    {
        "id": "web_html_002",
        "domain": "web_development",
        "skill": "HTML",
        "difficulty": "medium",
        "question": "What is the purpose and SEO significance of using `alt` attributes on `<img>` tags?",
        "options": [
            {"id": "A", "text": "It scales the image size to fit screen bounds."},
            {"id": "B", "text": "It provides a text description for screen readers (accessibility) and helps search engine crawlers index the image context correctly."},
            {"id": "C", "text": "It compiles CSS styles inside the image container."},
            {"id": "D", "text": "It prevents scripts from executing inside the image src."}
        ],
        "correct_option_id": "B",
        "explanation": "Alt text ensures accessibility for visually impaired users using screen readers and serves as indexing text for search engine optimizations (SEO).",
        "weight": 1
    },
    {
        "id": "web_html_003",
        "domain": "web_development",
        "skill": "HTML",
        "difficulty": "hard",
        "question": "Explain the difference in document lifecycle and parsing behavior when using `<script src='...' async>` versus `<script src='...' defer>` tags.",
        "options": [
            {"id": "A", "text": "async executes scripts in alphabetical order; defer executes them randomly."},
            {"id": "B", "text": "async downloads the script in parallel and executes it immediately (blocking HTML parsing during execution); defer downloads in parallel but waits to execute until HTML document parsing is complete (maintaining script load order)."},
            {"id": "C", "text": "defer loads scripts asynchronously, while async blocks downloads during image parsing."},
            {"id": "D", "text": "There is no difference; they are aliases in modern browsers."}
        ],
        "correct_option_id": "B",
        "explanation": "Async script downloads don't block parsing but pause parsing the moment the script is downloaded to execute it immediately. Defer scripts guarantee download in parallel without pausing parsing, running strictly in source order after document parsing is done.",
        "weight": 1
    },

    # CSS
    {
        "id": "web_css_001",
        "domain": "web_development",
        "skill": "CSS",
        "difficulty": "easy",
        "question": "In the CSS Box Model, which property control spacing outside the border of an element?",
        "options": [
            {"id": "A", "text": "Padding"},
            {"id": "B", "text": "Margin"},
            {"id": "C", "text": "Content"},
            {"id": "D", "text": "Height"}
        ],
        "correct_option_id": "B",
        "explanation": "Padding handles spacing inside the border. Margin handles spacing outside the border of elements.",
        "weight": 1
    },
    {
        "id": "web_css_002",
        "domain": "web_development",
        "skill": "CSS",
        "difficulty": "medium",
        "question": "What is the default value of the `position` property in CSS, and how does it behave in the normal document flow?",
        "options": [
            {"id": "A", "text": "relative; positions elements relative to their parent container."},
            {"id": "B", "text": "static; the element is positioned according to the normal flow of the document (top, left, z-index have no effect)."},
            {"id": "C", "text": "absolute; removes the element from the normal document flow."},
            {"id": "D", "text": "fixed; pins the element to the viewport."}
        ],
        "correct_option_id": "B",
        "explanation": "The default position is static. Static elements sit in the normal document flow, ignoring properties like top, bottom, left, right, and z-index.",
        "weight": 1
    },
    {
        "id": "web_css_003",
        "domain": "web_development",
        "skill": "CSS",
        "difficulty": "hard",
        "question": "Explain the concept of CSS Specifity and calculate the specificity score of the selector: `div.content ul li a:hover`.",
        "options": [
            {"id": "A", "text": "Specificity is 0, 0, 1, 4 (one class/pseudo-class, four element selectors)."},
            {"id": "B", "text": "Specificity is 0, 0, 2, 4 (two classes/pseudo-classes: .content and :hover, and four elements: div, ul, li, a)."},
            {"id": "C", "text": "Specificity is 0, 1, 0, 0 (one ID selector overrides elements)."},
            {"id": "D", "text": "Specificity is 0, 0, 0, 6 (six tag names counted uniformly)."}
        ],
        "correct_option_id": "B",
        "explanation": "Specificity is calculated in components: (ID, Class/Attribute/Pseudo-class, Element/Pseudo-element). Here, we have two class-like components (`.content`, `:hover` pseudo-class) and four element tags (`div`, `ul`, `li`, `a`). Hence, score is (0, 2, 4).",
        "weight": 1
    },

    # JavaScript
    {
        "id": "web_js_001",
        "domain": "web_development",
        "skill": "JavaScript",
        "difficulty": "easy",
        "question": "Which JavaScript keyword is used to declare block-scoped variables that cannot be reassigned?",
        "options": [
            {"id": "A", "text": "var"},
            {"id": "B", "text": "let"},
            {"id": "C", "text": "const"},
            {"id": "D", "text": "function"}
        ],
        "correct_option_id": "C",
        "explanation": "const declares block-scoped variables that cannot be reassigned, although objects/arrays declared with const can still have their properties mutated.",
        "weight": 1
    },
    {
        "id": "web_js_002",
        "domain": "web_development",
        "skill": "JavaScript",
        "difficulty": "medium",
        "question": "Explain how event delegation works in JavaScript DOM manipulation.",
        "options": [
            {"id": "A", "text": "By adding event listeners to every single child element in the document tree manually."},
            {"id": "B", "text": "By attaching a single event listener to a parent element, leveraging event bubbling to catch events fired by child elements through `event.target`."},
            {"id": "C", "text": "By executing event handlers inside async web worker tasks."},
            {"id": "D", "text": "By calling `event.stopPropagation()` on all window clicks."}
        ],
        "correct_option_id": "B",
        "explanation": "Event delegation leverages event bubbling. Instead of adding listeners to 100 buttons, you add 1 listener to the container. Clicks on buttons bubble up to the container, which processes them.",
        "weight": 1
    },
    {
        "id": "web_js_003",
        "domain": "web_development",
        "skill": "JavaScript",
        "difficulty": "hard",
        "question": "What is a Closure in JavaScript, and what memory management issues can it potentially introduce in long-lived applications?",
        "options": [
            {"id": "A", "text": "Closures compile functions to binary formats; they trigger stack overflow errors."},
            {"id": "B", "text": "A closure is a function that retains access to its lexical scope even when executed outside that scope; they can cause memory leaks by preventing the garbage collector from freeing variables in parent scopes if the closure persists in memory."},
            {"id": "C", "text": "A closure is an API call; it causes network memory exhaustion."},
            {"id": "D", "text": "It is when you close the browser window; it releases all RAM."}
        ],
        "correct_option_id": "B",
        "explanation": "A closure preserves variables of its outer scope because the inner function references them. If the inner function is kept alive (e.g. in a global list or event listener), the outer variables cannot be garbage collected, creating memory leaks.",
        "weight": 1
    },

    # DOM
    {
        "id": "web_dom_001",
        "domain": "web_development",
        "skill": "DOM",
        "difficulty": "easy",
        "question": "Which DOM method is used to select an element by its ID attribute in vanilla JavaScript?",
        "options": [
            {"id": "A", "text": "document.querySelectorClass()"},
            {"id": "B", "text": "document.getElementById()"},
            {"id": "C", "text": "document.findId()"},
            {"id": "D", "text": "document.createElement()"}
        ],
        "correct_option_id": "B",
        "explanation": "document.getElementById(id) returns the Element object whose id property matches the specified string.",
        "weight": 1
    },
    {
        "id": "web_dom_002",
        "domain": "web_development",
        "skill": "DOM",
        "difficulty": "medium",
        "question": "What is the key performance difference between writing directly to `innerHTML` and using `document.createElement()` with `appendChild()`?",
        "options": [
            {"id": "A", "text": "innerHTML is faster because it bypasses the browser parser."},
            {"id": "B", "text": "innerHTML parses the string as HTML, destroying and rebuilding the entire DOM tree of the target container, causing poor performance and potential XSS vulnerability, while appendChild() manipulates nodes directly."},
            {"id": "C", "text": "appendChild() requires CSS stylesheets to be re-parsed, making it slower."},
            {"id": "D", "text": "There is no difference; browsers execute them identically."}
        ],
        "correct_option_id": "B",
        "explanation": "Writing to `innerHTML` invokes the HTML parser for the entire content string, resetting all child nodes (losing event listeners). Direct node methods manipulate the DOM tree directly without full parsing, protecting against XSS.",
        "weight": 1
    },
    {
        "id": "web_dom_003",
        "domain": "web_development",
        "skill": "DOM",
        "difficulty": "hard",
        "question": "What is layout thrashing (forced synchronous layout) in web browsers, and how do you prevent it in animations?",
        "options": [
            {"id": "A", "text": "It is when too many DOM nodes are deleted; resolved by using virtual nodes."},
            {"id": "B", "text": "It is when JavaScript writes to DOM styles then reads layout properties (e.g. offsetHeight) in quick succession, forcing the browser to calculate layout multiple times inside a single frame; prevented by batching reads and batching writes (e.g. using FastDOM or requestAnimationFrame)."},
            {"id": "C", "text": "It is network traffic congestion; resolved by using throttling APIs."},
            {"id": "D", "text": "It is when images load slower than text; resolved by applying alt attributes."}
        ],
        "correct_option_id": "B",
        "explanation": " forced synchronous layout occurs when you style an element (write) and query its physical size (read) in a loop. The browser is forced to reflow layout on demand to give accurate reads. Batching reads first, then writes in `requestAnimationFrame` fixes this.",
        "weight": 1
    },

    # HTTP & REST APIs
    {
        "id": "web_http_001",
        "domain": "web_development",
        "skill": "HTTP & REST APIs",
        "difficulty": "easy",
        "question": "Which HTTP method is designed for creating new resources in a RESTful API architecture?",
        "options": [
            {"id": "A", "text": "GET"},
            {"id": "B", "text": "POST"},
            {"id": "C", "text": "PUT"},
            {"id": "D", "text": "DELETE"}
        ],
        "correct_option_id": "B",
        "explanation": "In REST, POST is standard for submitting data to a resource to create a new record entry.",
        "weight": 1
    },
    {
        "id": "web_http_002",
        "domain": "web_development",
        "skill": "HTTP & REST APIs",
        "difficulty": "medium",
        "question": "Explain the difference in idempotency between HTTP PUT and PATCH methods.",
        "options": [
            {"id": "A", "text": "PUT is idempotent (replacing the entire resource); PATCH is generally non-idempotent (applying partial updates)."},
            {"id": "B", "text": "PATCH is idempotent, and PUT is non-idempotent."},
            {"id": "C", "text": "Both methods are non-idempotent in all circumstances."},
            {"id": "D", "text": "PUT only works with JSON data, whereas PATCH only works with XML."}
        ],
        "correct_option_id": "A",
        "explanation": "PUT replaces the resource entirely. Running it multiple times yields identical results (idempotent). PATCH applies partial edits; depending on the operation, repeating it may alter the state (e.g. append updates).",
        "weight": 1
    },
    {
        "id": "web_http_003",
        "domain": "web_development",
        "skill": "HTTP & REST APIs",
        "difficulty": "hard",
        "question": "Explain how CORS (Cross-Origin Resource Sharing) preflight requests function and when they are triggered by the browser.",
        "options": [
            {"id": "A", "text": "Preflight is an HTTP GET query triggered automatically for simple forms to cache stylesheets."},
            {"id": "B", "text": "Preflight is an HTTP OPTIONS request sent by the browser to verify permissions before the actual request is sent, triggered for non-simple requests (e.g., using custom headers like Authorization or methods like PUT/DELETE)."},
            {"id": "C", "text": "Preflight checks database indexes using SQL scripts."},
            {"id": "D", "text": "Preflight executes only when servers return a 500 error status."}
        ],
        "correct_option_id": "B",
        "explanation": "Before sending requests that could mutate data or use custom parameters, browsers send an OPTIONS preflight to verify if the origin has server permissions, securing APIs against unauthorized cross-site scripts.",
        "weight": 1
    },

    # React
    {
        "id": "web_react_001",
        "domain": "web_development",
        "skill": "React",
        "difficulty": "easy",
        "question": "Which React hook is used to perform side effects (e.g. data fetching) in functional components?",
        "options": [
            {"id": "A", "text": "useState"},
            {"id": "B", "text": "useEffect"},
            {"id": "C", "text": "useContext"},
            {"id": "D", "text": "useMemo"}
        ],
        "correct_option_id": "B",
        "explanation": "useEffect lets you synchronize a component with an external system (side effects, subscriptions, API fetching).",
        "weight": 1
    },
    {
        "id": "web_react_002",
        "domain": "web_development",
        "skill": "React",
        "difficulty": "medium",
        "question": "In React, why must you avoid mutating state variables directly (e.g. calling `state.push(item)`) instead of using setter functions?",
        "options": [
            {"id": "A", "text": "Direct mutations will cause the browser to crash immediately."},
            {"id": "B", "text": "React relies on reference comparison of state to trigger re-renders; mutating objects in-place does not change reference, preventing UI updates."},
            {"id": "C", "text": "Mutations violate CSS specificity rules."},
            {"id": "D", "text": "Setters compress values into local storage automatically."}
        ],
        "correct_option_id": "B",
        "explanation": "React compares old and new state references (`Object.is`). Mutating arrays or objects in place keeps the same reference, so React assumes no state change occurred, ignoring re-renders.",
        "weight": 1
    },
    {
        "id": "web_react_003",
        "domain": "web_development",
        "skill": "React",
        "difficulty": "hard",
        "question": "What is the function of the `key` prop in React lists, and what are the performance and state bugs introduced by using array indexes as keys?",
        "options": [
            {"id": "A", "text": "Keys act as CSS styles; indexes slow down style evaluations."},
            {"id": "B", "text": "Keys help React identify which items changed, added, or removed; using array index as a key can cause rendering bugs and state inconsistency when list order changes (reordering, prepending) because React correlates state to index positions."},
            {"id": "C", "text": "Keys prevent external API queries from executing twice during render cycles."},
            {"id": "D", "text": "Keys encrypt component tags for search engines."}
        ],
        "correct_option_id": "B",
        "explanation": "React uses keys to track node identity. If you prepend an item to a list and use index as key, React sees index 0 exist before and after, map-linking the existing state of old index 0 to the new prepended element, causing visual/input bugs.",
        "weight": 1
    },

    # State Management
    {
        "id": "web_state_001",
        "domain": "web_development",
        "skill": "State Management",
        "difficulty": "easy",
        "question": "What is 'prop drilling' in React application architectures?",
        "options": [
            {"id": "A", "text": "Accessing state stored in local storage"},
            {"id": "B", "text": "Passing props down through multiple layers of nested components to reach a deeply nested child"},
            {"id": "C", "text": "Rendering lists using map functions"},
            {"id": "D", "text": "Debugging API calls in the browser"}
        ],
        "correct_option_id": "B",
        "explanation": "Prop drilling is passing props through intermediary components that don't need the data themselves, purely to pass it to lower components.",
        "weight": 1
    },
    {
        "id": "web_state_002",
        "domain": "web_development",
        "skill": "State Management",
        "difficulty": "medium",
        "question": "When is it appropriate to use a global state manager (like Redux or Zustand) instead of standard React Context API?",
        "options": [
            {"id": "A", "text": "When you only have static layout variables."},
            {"id": "B", "text": "When you have high-frequency state updates in large applications, because Context triggers re-renders on all consumers on any value update, causing performance bottlenecks."},
            {"id": "C", "text": "Zustand is required to fetch REST API data securely."},
            {"id": "D", "text": "Only when working with class components."}
        ],
        "correct_option_id": "B",
        "explanation": "Context isn't optimized for high-frequency updates. Changing context forces all consumer components to re-render. State managers use selectors to ensure components only re-render when their specific sliced data updates.",
        "weight": 1
    },
    {
        "id": "web_state_003",
        "domain": "web_development",
        "skill": "State Management",
        "difficulty": "hard",
        "question": "Explain the architectural differences and performance implications of Unidirectional Data Flow (Redux) versus Proxy-based reactive state (Zustand/MobX).",
        "options": [
            {"id": "A", "text": "Proxy state requires compiling code at runtime, while unidirectional flow executes natively in browsers."},
            {"id": "B", "text": "Redux uses immutable states with central reducers and dispatch actions, ensuring highly predictable state logs; MobX uses observable properties and proxy get/set intercepts to track dependencies and trigger precise granular updates dynamically, which can be faster but harder to debug."},
            {"id": "C", "text": "Zustand uses SQLite databases in the browser, while Redux uses files."},
            {"id": "D", "text": "Proxy-based state management is only supported in Node.js backends."}
        ],
        "correct_option_id": "B",
        "explanation": "Redux uses actions/reducers to build new states immutably. MobX wraps state in JS Proxies; reading values links components to properties, and mutating values triggers re-renders automatically for those specific components, bypassing virtual DOM diffing paths.",
        "weight": 1
    },

    # Backend Fundamentals
    {
        "id": "web_back_001",
        "domain": "web_development",
        "skill": "Backend Fundamentals",
        "difficulty": "easy",
        "question": "What is the primary difference between a process and a thread in operating system backend architectures?",
        "options": [
            {"id": "A", "text": "Threads contain processes; processes run in memory."},
            {"id": "B", "text": "A process has its own isolated memory space, while threads within a process share the same memory space."},
            {"id": "C", "text": "Processes are only used for databases, and threads handle HTTP queries."},
            {"id": "D", "text": "Processes are virtual; threads are hardware components."}
        ],
        "correct_option_id": "B",
        "explanation": "Processes run isolated. Sharing data requires IPC (Inter-Process Communication). Threads run inside a process and share its address space, making communication fast but prone to race conditions.",
        "weight": 1
    },
    {
        "id": "web_back_002",
        "domain": "web_development",
        "skill": "Backend Fundamentals",
        "difficulty": "medium",
        "question": "How does an Event Loop (like Node.js or Python asyncio) handle thousands of concurrent I/O connections using only a single thread?",
        "options": [
            {"id": "A", "text": "It runs queries in separate child processes behind the scenes."},
            {"id": "B", "text": "It delegates blocking I/O calls to the operating system kernel (using epoll/kqueue) and registers callbacks, running JavaScript/Python code sequentially without waiting for connections to respond."},
            {"id": "C", "text": "It automatically increases thread counts based on CPU cores."},
            {"id": "D", "text": "It converts files to local memory buffers."}
        ],
        "correct_option_id": "B",
        "explanation": "Non-blocking I/O registers callbacks in the OS kernel. The event loop continuously polls the OS for finished I/O events, executing callbacks sequentially in a single thread, avoiding thread switching context overhead.",
        "weight": 1
    },
    {
        "id": "web_back_003",
        "domain": "web_development",
        "skill": "Backend Fundamentals",
        "difficulty": "hard",
        "question": "What is horizontal scaling versus vertical scaling of web backends, and what architectural challenges does horizontal scaling introduce for session management?",
        "options": [
            {"id": "A", "text": "Vertical scaling requires database clusters; horizontal scaling is strictly a CSS design pattern."},
            {"id": "B", "text": "Vertical scaling adds resources (CPU/RAM) to a single server; horizontal scaling adds more server nodes, which requires moving session state from local server memory to a shared distributed cache (like Redis) so requests from the same user are session-aware on any server."},
            {"id": "C", "text": "Horizontal scaling requires rewriting code in C++; vertical scaling runs automatically on docker containers."},
            {"id": "D", "text": "Vertical scaling is cheaper; horizontal scaling eliminates database locks."}
        ],
        "correct_option_id": "B",
        "explanation": "Horizontal scaling distributes load. Because requests can hit any server node, storing session state in a server's local memory (e.g. local dict) breaks authorization. A centralized session store (Redis) resolves this.",
        "weight": 1
    },

    # Authentication
    {
        "id": "web_auth_001",
        "domain": "web_development",
        "skill": "Authentication",
        "difficulty": "easy",
        "question": "What are the three components of a JSON Web Token (JWT)?",
        "options": [
            {"id": "A", "text": "Username, Password, Salt"},
            {"id": "B", "text": "Header, Payload, Signature"},
            {"id": "C", "text": "Host, Request, Response"},
            {"id": "D", "text": "Client, Server, Database"}
        ],
        "correct_option_id": "B",
        "explanation": "A JWT is a dot-separated string containing a base64url-encoded Header (metadata), Payload (claims), and a Signature (verifiability).",
        "weight": 1
    },
    {
        "id": "web_auth_002",
        "domain": "web_development",
        "skill": "Authentication",
        "difficulty": "medium",
        "question": "What is the difference between Authentication and Authorization in security architectures?",
        "options": [
            {"id": "A", "text": "Authentication is verifying who a user is (identity), while Authorization is verifying what specific resources or actions they are allowed to access (permissions)."},
            {"id": "B", "text": "Authorization is identifying users, and Authentication is logging out."},
            {"id": "C", "text": "Authentication is client-side validation; Authorization is database checks."},
            {"id": "D", "text": "There is no difference; they are synonymous."}
        ],
        "correct_option_id": "A",
        "explanation": "Authentication validates identity credentials (e.g. login). Authorization maps validated identities to access control policies (permissions).",
        "weight": 1
    },
    {
        "id": "web_auth_003",
        "domain": "web_development",
        "skill": "Authentication",
        "difficulty": "hard",
        "question": "Explain the security differences between storing JWTs in browser `localStorage` versus in `httpOnly` secure Cookies, specifically regarding XSS and CSRF attacks.",
        "options": [
            {"id": "A", "text": "localStorage protects against XSS; httpOnly cookies protect against CSRF."},
            {"id": "B", "text": "localStorage is vulnerable to XSS (malicious scripts can read the token directly); httpOnly cookies protect against XSS by hiding the token from client-side JavaScript, but introduce vulnerability to CSRF (Cross-Site Request Forgery), which must be mitigated using SameSite attributes and anti-CSRF tokens."},
            {"id": "C", "text": "Cookies only support string tokens, while localStorage supports JSON objects."},
            {"id": "D", "text": "httpOnly cookies are obsolete; modern browsers block them entirely."}
        ],
        "correct_option_id": "B",
        "explanation": "httpOnly cookies hide contents from Javascript, protecting against XSS token theft. However, browsers send cookies automatically on all requests to that domain, making them vulnerable to CSRF. CSRF is blocked using SameSite=Strict and custom headers.",
        "weight": 1
    },

    # Databases
    {
        "id": "web_db_001",
        "domain": "web_development",
        "skill": "Databases",
        "difficulty": "easy",
        "question": "Which database type stores data in structured tables with primary and foreign keys to enforce relationships?",
        "options": [
            {"id": "A", "text": "NoSQL Database"},
            {"id": "B", "text": "Relational (SQL) Database"},
            {"id": "C", "text": "Graph Database"},
            {"id": "D", "text": "Key-Value Store"}
        ],
        "correct_option_id": "B",
        "explanation": "Relational databases use tables, rows, columns, and foreign keys to define data relations.",
        "weight": 1
    },
    {
        "id": "web_db_002",
        "domain": "web_development",
        "skill": "Databases",
        "difficulty": "medium",
        "question": "What are ACID properties in database transaction management?",
        "options": [
            {"id": "A", "text": "Algorithms, Clusters, Indexes, Directories"},
            {"id": "B", "text": "Atomicity, Consistency, Isolation, Durability"},
            {"id": "C", "text": "Aggregation, Coding, Interface, Deployment"},
            {"id": "D", "text": "Access, Compression, Integrity, Duplication"}
        ],
        "correct_option_id": "B",
        "explanation": "ACID properties guarantee database transactions are processed reliably: Atomicity (all or nothing), Consistency (preserves rules), Isolation (independent runs), Durability (persisted outcomes).",
        "weight": 1
    },
    {
        "id": "web_db_003",
        "domain": "web_development",
        "skill": "Databases",
        "difficulty": "hard",
        "question": "Explain the architectural trade-offs between SQL (Relational) and NoSQL (Document) databases regarding schema flexibility and scaling.",
        "options": [
            {"id": "A", "text": "NoSQL does not support queries; SQL databases only scale horizontally."},
            {"id": "B", "text": "SQL databases enforce strict schemas and referential integrity, scaling primarily vertically (expensive); NoSQL databases provide schema flexibility (dynamic JSON documents) and scale horizontally by partitioning data across nodes easily, but sacrifice strict cross-document consistency."},
            {"id": "C", "text": "SQL databases scale horizontally by default, and NoSQL only scales vertically."},
            {"id": "D", "text": "NoSQL is always faster because it does not support disk writes."}
        ],
        "correct_option_id": "B",
        "explanation": "SQL is designed for relational consistency (joins). Scaling horizontally requires complex sharding. NoSQL document databases partition data naturally across nodes since documents are self-contained, but don't support ACID across distributed records.",
        "weight": 1
    }
]

# 5. CLOUD & DEVOPS QUESTIONS
devops_questions = [
    # Linux
    {
        "id": "devops_linux_001",
        "domain": "cloud_devops",
        "skill": "Linux",
        "difficulty": "easy",
        "question": "Which Linux command is used to display the contents of a text file to the terminal screen?",
        "options": [
            {"id": "A", "text": "ls"},
            {"id": "B", "text": "cat"},
            {"id": "C", "text": "pwd"},
            {"id": "D", "text": "grep"}
        ],
        "correct_option_id": "B",
        "explanation": "`cat` (concatenate) prints files to stdout.",
        "weight": 1
    },
    {
        "id": "devops_linux_002",
        "domain": "cloud_devops",
        "skill": "Linux",
        "difficulty": "medium",
        "question": "In Linux file permissions, what does `chmod 755 filename` accomplish?",
        "options": [
            {"id": "A", "text": "Grants read/write/execute to owner, and read/execute to group and others."},
            {"id": "B", "text": "Grants full permissions (read/write/execute) to everyone."},
            {"id": "C", "text": "Restricts all access to the file except for root."},
            {"id": "D", "text": "Sets the file size to 755 kilobytes."}
        ],
        "correct_option_id": "A",
        "explanation": "755 translates to binary octals: Owner gets 7 (rwx), Group gets 5 (r-x), Others get 5 (r-x).",
        "weight": 1
    },
    {
        "id": "devops_linux_003",
        "domain": "cloud_devops",
        "skill": "Linux",
        "difficulty": "hard",
        "question": "What is the difference between a hard link and a soft (symbolic) link in Linux filesystems?",
        "options": [
            {"id": "A", "text": "Hard links are for directories only; soft links are for files."},
            {"id": "B", "text": "A hard link points directly to the file inode (sharing physical disk blocks) and survives deletion of the original file path; a soft link is a path-pointer that becomes a broken link if the target is deleted."},
            {"id": "C", "text": "Soft links allocate physical disk space for files, while hard links compile code."},
            {"id": "D", "text": "Hard links are encrypted; soft links are clear text."}
        ],
        "correct_option_id": "B",
        "explanation": "Hard links share the same inode number. Deleting the original name leaves the hard link intact. Soft links point to the pathname; if target pathname is renamed or deleted, the soft link points to a non-existent path.",
        "weight": 1
    },

    # Networking
    {
        "id": "devops_net_001",
        "domain": "cloud_devops",
        "skill": "Networking",
        "difficulty": "easy",
        "question": "What is the primary function of DNS (Domain Name System) in computer networking?",
        "options": [
            {"id": "A", "text": "Encrypt HTTP traffic"},
            {"id": "B", "text": "Translate human-readable domain names to numerical IP addresses"},
            {"id": "C", "text": "Assign dynamic IP addresses to client devices"},
            {"id": "D", "text": "Route packets between different subnets"}
        ],
        "correct_option_id": "B",
        "explanation": "DNS acts as a phone book for the internet, resolving domain names (e.g. google.com) to IP addresses (e.g. 142.250.190.46).",
        "weight": 1
    },
    {
        "id": "devops_net_002",
        "domain": "cloud_devops",
        "skill": "Networking",
        "difficulty": "medium",
        "question": "What is a subnet mask (e.g., /24 in CIDR notation) used for in IP routing?",
        "options": [
            {"id": "A", "text": "To hide the IP address of the server from search engines."},
            {"id": "B", "text": "To divide an IP address into network portion and host portion, determining which IPs belong to the local subnet."},
            {"id": "C", "text": "To encrypt packets at the transport layer."},
            {"id": "D", "text": "To adjust the bandwidth speeds of network cables."}
        ],
        "correct_option_id": "B",
        "explanation": "/24 CIDR means the first 24 bits represent the network prefix (e.g. 255.255.255.0). Any IP sharing these 24 bits is local; other targets route through the default gateway.",
        "weight": 1
    },
    {
        "id": "devops_net_003",
        "domain": "cloud_devops",
        "skill": "Networking",
        "difficulty": "hard",
        "question": "Explain the fundamental difference between TCP and UDP at the Transport layer, and how they handle packet loss.",
        "options": [
            {"id": "A", "text": "UDP uses handshakes to recover lost packets; TCP ignores drops to prioritize speeds."},
            {"id": "B", "text": "TCP is connection-oriented, ensuring reliable packet delivery via handshakes, sequencing, and retransmissions when loss is detected; UDP is connectionless and sends packets immediately without tracking delivery or retransmitting drops, prioritizing low latency over reliability."},
            {"id": "C", "text": "TCP operates at Layer 3; UDP operates at Layer 7."},
            {"id": "D", "text": "TCP is only used for local networks, whereas UDP routes across the internet."}
        ],
        "correct_option_id": "B",
        "explanation": "TCP builds sessions (3-way handshake). It expects ACKs for packets; if an ACK is missing, it triggers retransmissions. UDP dumps packets to targets directly, making it optimal for video streams where speed matters more than occasional pixel drops.",
        "weight": 1
    },

    # Git
    {
        "id": "devops_git_001",
        "domain": "cloud_devops",
        "skill": "Git",
        "difficulty": "easy",
        "question": "Which Git command is used to fetch changes from a remote repository and integrate them immediately into the current local branch?",
        "options": [
            {"id": "A", "text": "git push"},
            {"id": "B", "text": "git pull"},
            {"id": "C", "text": "git commit"},
            {"id": "D", "text": "git fetch"}
        ],
        "correct_option_id": "B",
        "explanation": "`git pull` is a shortcut for running `git fetch` followed immediately by `git merge` on the target remote branch.",
        "weight": 1
    },
    {
        "id": "devops_git_002",
        "domain": "cloud_devops",
        "skill": "Git",
        "difficulty": "medium",
        "question": "What is the difference between `git merge` and `git rebase` when integrating changes from a feature branch?",
        "options": [
            {"id": "A", "text": "merge deletes the branch; rebase keeps it."},
            {"id": "B", "text": "merge combines branches by creating a new merge commit (preserving historical commit sequence); rebase applies feature commits sequentially on top of the target branch tip, writing a clean, linear commit history."},
            {"id": "C", "text": "rebase is slower because it uploads files to GitHub."},
            {"id": "D", "text": "merge only works with single commits."}
        ],
        "correct_option_id": "B",
        "explanation": "Merge retains the historical branch graph showing exact splits. Rebase rewrites history by changing the base commit of the feature branch to the head of target (e.g. main), creating a clean linear path.",
        "weight": 1
    },
    {
        "id": "devops_git_003",
        "domain": "cloud_devops",
        "skill": "Git",
        "difficulty": "hard",
        "question": "What does `git reset --hard HEAD~1` accomplish, and what are the risks of using it on a shared remote branch?",
        "options": [
            {"id": "A", "text": "It renames the branch; has no risk since remote is untouched."},
            {"id": "B", "text": "It deletes the latest commit, resetting the working directory and staging index; if pushed to a shared remote, it rewrites history, forcing other developers out of sync and causing merge conflicts during pulls."},
            {"id": "C", "text": "It resets only configuration files, maintaining commit history safely."},
            {"id": "D", "text": "It creates a backup of the branch under a hidden folder."}
        ],
        "correct_option_id": "B",
        "explanation": "The `--hard` flag discards all changes. Running it deletes the latest commit from history. Pushing this remote requires `--force`, which breaks coworkers' clones because commits they pulled are deleted.",
        "weight": 1
    },

    # Docker
    {
        "id": "devops_docker_001",
        "domain": "cloud_devops",
        "skill": "Docker",
        "difficulty": "easy",
        "question": "Which Dockerfile instruction specifies the default command executed when a container starts up?",
        "options": [
            {"id": "A", "text": "RUN"},
            {"id": "B", "text": "FROM"},
            {"id": "C", "text": "CMD"},
            {"id": "D", "text": "COPY"}
        ],
        "correct_option_id": "C",
        "explanation": "CMD sets the entry point executable command for container executions (e.g. `CMD ['python', 'app.py']`). RUN runs commands during the image build process.",
        "weight": 1
    },
    {
        "id": "devops_docker_002",
        "domain": "cloud_devops",
        "skill": "Docker",
        "difficulty": "medium",
        "question": "In Docker, what is the conceptual difference between an Image and a Container?",
        "options": [
            {"id": "A", "text": "An image is a running instance, and a container is the static blueprint."},
            {"id": "B", "text": "An image is a read-only, static package template containing app code and dependencies; a container is a live, writeable execution instance of that image running in isolated namespace processes."},
            {"id": "C", "text": "Images are stored on servers; containers can only run locally."},
            {"id": "D", "text": "Images are virtual machines; containers are physical servers."}
        ],
        "correct_option_id": "B",
        "explanation": "Images are blueprints (read-only layers). Containers are active instances of these images running with a read-write layer on top to handle system outputs.",
        "weight": 1
    },
    {
        "id": "devops_docker_003",
        "domain": "cloud_devops",
        "skill": "Docker",
        "difficulty": "hard",
        "question": "How does Docker leverage Linux kernel namespaces and control groups (cgroups) to isolate container processes?",
        "options": [
            {"id": "A", "text": "Namespaces compile code to assembly; cgroups translate network addresses."},
            {"id": "B", "text": "Namespaces provide isolation of system resources (PID, NET, MNT, IPC) so a container only sees its own processes; cgroups enforce resource limits (CPU, RAM, I/O bandwidth) to prevent resource hogging."},
            {"id": "C", "text": "cgroups encrypt files on disk, while namespaces block root ports."},
            {"id": "D", "text": "Both mechanisms perform virtual machine bios hypervisor operations."}
        ],
        "correct_option_id": "B",
        "explanation": "Namespaces ensure container processes cannot see or interfere with files, networks, or process trees of the host or other containers. Cgroups throttle physical CPU/RAM consumption to enforce resource quotas.",
        "weight": 1
    },

    # Containers
    {
        "id": "devops_cont_001",
        "domain": "cloud_devops",
        "skill": "Containers",
        "difficulty": "easy",
        "question": "What is the primary purpose of a container registry (e.g. Docker Hub)?",
        "options": [
            {"id": "A", "text": "To compile container source code"},
            {"id": "B", "text": "To store, version, and distribute built container images"},
            {"id": "C", "text": "To monitor CPU usage of active servers"},
            {"id": "D", "text": "To edit code files directly in production"}
        ],
        "correct_option_id": "B",
        "explanation": "Registries act as central storage depots from which deployment targets pull container images to instantiate containers.",
        "weight": 1
    },
    {
        "id": "devops_cont_002",
        "domain": "cloud_devops",
        "skill": "Containers",
        "difficulty": "medium",
        "question": "Why is running a container as root (UID 0) inside production environments considered a severe security risk?",
        "options": [
            {"id": "A", "text": "It causes the container to crash if memory usage spikes."},
            {"id": "B", "text": "If a hacker escapes the container process, they automatically gain root permissions on the host system, compromising the entire host node."},
            {"id": "C", "text": "Root containers cannot route network queries through ports."},
            {"id": "D", "text": "It forces images to double their file sizes."}
        ],
        "correct_option_id": "B",
        "explanation": "Container root matches host root. If container escaping vulnerabilities occur, the intruder gains full host access. Restricting processes to non-root users inside Dockerfiles mitigates this.",
        "weight": 1
    },
    {
        "id": "devops_cont_003",
        "domain": "cloud_devops",
        "skill": "Containers",
        "difficulty": "hard",
        "question": "Explain the concept of 'multi-stage builds' in Dockerfiles and how they optimize build footprints.",
        "options": [
            {"id": "A", "text": "Using multiple base images to build separate containers in parallel."},
            {"id": "B", "text": "Using separate `FROM` instructions, allowing developers to use heavy build environments (with compilers/SDKs) in early stages, and copying only the compiled artifacts into a lightweight production stage (e.g. alpine), leaving build tools behind."},
            {"id": "C", "text": "Uploading files to multiple container registries during the run step."},
            {"id": "D", "text": "Scaling containers vertically before compilation."}
        ],
        "correct_option_id": "B",
        "explanation": "Multi-stage builds use different images. For example, you build a Go app in `golang:latest` (800MB), and copy only the compiled binary to `alpine` (5MB). The final production image excludes compilers, reducing attack surfaces and footprints.",
        "weight": 1
    },

    # CI/CD
    {
        "id": "devops_cicd_001",
        "domain": "cloud_devops",
        "skill": "CI/CD",
        "difficulty": "easy",
        "question": "What does Continuous Integration (CI) focus on in development lifecycles?",
        "options": [
            {"id": "A", "text": "Manually testing code in production environments"},
            {"id": "B", "text": "Automatically building, testing, and merging code changes into a shared repository to detect integration errors early"},
            {"id": "C", "text": "Deploying servers to different geographic regions"},
            {"id": "D", "text": "Managing developer salaries and calendars"}
        ],
        "correct_option_id": "B",
        "explanation": "CI automates build/test triggers on every code commit, ensuring code integrates cleanly before branch merges.",
        "weight": 1
    },
    {
        "id": "devops_cicd_002",
        "domain": "cloud_devops",
        "skill": "CI/CD",
        "difficulty": "medium",
        "question": "What is the difference between Continuous Delivery and Continuous Deployment?",
        "options": [
            {"id": "A", "text": "Delivery runs tests; Deployment does not."},
            {"id": "B", "text": "Continuous Delivery prepares code and automatically builds it, requiring manual approval to push to production; Continuous Deployment automates the entire process, releasing changes to production without human intervention after passing tests."},
            {"id": "C", "text": "Delivery deploys databases; Deployment only deploys static files."},
            {"id": "D", "text": "Continuous Deployment is for local environments only."}
        ],
        "correct_option_id": "B",
        "explanation": "Delivery keeps code deployable at any time, requiring a manual trigger. Deployment removes this manual step, automatically pushing every verified commit through the pipeline into production.",
        "weight": 1
    },
    {
        "id": "devops_cicd_003",
        "domain": "cloud_devops",
        "skill": "CI/CD",
        "difficulty": "hard",
        "question": "Explain the concept of 'blue-green deployment' in CI/CD pipeline strategies and how it minimizes production downtime.",
        "options": [
            {"id": "A", "text": "Running half of the code in dark mode (blue) and half in light mode (green)."},
            {"id": "B", "text": "Maintaining two identical production environments (Blue is live, Green is idle); new code is deployed to Green, tested, and a router switches traffic to Green, making it live. If failures occur, traffic is routed back to Blue immediately, yielding zero downtime."},
            {"id": "C", "text": "Dividing databases into SQL and NoSQL targets during build steps."},
            {"id": "D", "text": "Deploying servers in alternate timezone schedules."}
        ],
        "correct_option_id": "B",
        "explanation": "Blue-green deployment uses redundant environments. Deploying to the idle environment permits testing. Swapping traffic via load balancers is instantaneous, providing zero-downtime releases and rapid rollback.",
        "weight": 1
    },

    # Cloud Fundamentals
    {
        "id": "devops_cloud_001",
        "domain": "cloud_devops",
        "skill": "Cloud Fundamentals",
        "difficulty": "easy",
        "question": "Which cloud computing model provides virtualized computing resources over the internet, like raw VMs (e.g. AWS EC2)?",
        "options": [
            {"id": "A", "text": "Software as a Service (SaaS)"},
            {"id": "B", "text": "Platform as a Service (PaaS)"},
            {"id": "C", "text": "Infrastructure as a Service (IaaS)"},
            {"id": "D", "text": "Functions as a Service (FaaS)"}
        ],
        "correct_option_id": "C",
        "explanation": "IaaS provides raw compute, network, and storage resources (e.g. AWS EC2, GCP Compute Engine).",
        "weight": 1
    },
    {
        "id": "devops_cloud_002",
        "domain": "cloud_devops",
        "skill": "Cloud Fundamentals",
        "difficulty": "medium",
        "question": "Explain the difference between vertical scaling (scaling up) and horizontal scaling (scaling out) in cloud architectures.",
        "options": [
            {"id": "A", "text": "Scaling up requires migrating to different cloud providers; scaling out is automatic."},
            {"id": "B", "text": "Scaling up means adding more RAM or CPU to an existing single virtual machine; scaling out means adding more virtual machines in parallel behind a load balancer."},
            {"id": "C", "text": "Scaling out is for storage disks; scaling up is for databases."},
            {"id": "D", "text": "Scaling up is cheap; scaling out requires Docker containers."}
        ],
        "correct_option_id": "B",
        "explanation": "Scaling up hits hardware limits and requires downtime. Scaling out scales infinitely by distributing traffic across multiple running nodes using a load balancer.",
        "weight": 1
    },
    {
        "id": "devops_cloud_003",
        "domain": "cloud_devops",
        "skill": "Cloud Fundamentals",
        "difficulty": "hard",
        "question": "What is the Shared Responsibility Model in cloud computing, and how is responsibility typically split for an IaaS deployment?",
        "options": [
            {"id": "A", "text": "The client handles hardware cooling; the cloud provider handles code compilation."},
            {"id": "B", "text": "The cloud provider handles security OF the cloud (physical security, virtualization, global infrastructure); the customer handles security IN the cloud (OS updates, firewall rules, data encryption, application code)."},
            {"id": "C", "text": "The provider assumes 100% of all liability for data breaches."},
            {"id": "D", "text": "Responsibilities are divided based on monthly billing limits."}
        ],
        "correct_option_id": "B",
        "explanation": "In IaaS (like AWS EC2), the vendor secures the physical hypervisors. However, the OS configuration, network ports (Security Groups), patches, database setups, and app vulnerabilities are entirely the customer's responsibility.",
        "weight": 1
    },

    # Virtual Machines
    {
        "id": "devops_vm_001",
        "domain": "cloud_devops",
        "skill": "Virtual Machines",
        "difficulty": "easy",
        "question": "What is the software component that creates and runs virtual machines on physical host hardware?",
        "options": [
            {"id": "A", "text": "Kernel"},
            {"id": "B", "text": "Hypervisor"},
            {"id": "C", "text": "BIOS"},
            {"id": "D", "text": "Docker Engine"}
        ],
        "correct_option_id": "B",
        "explanation": "A hypervisor (e.g. KVM, ESXi, Hyper-V) splits physical hardware into virtual slots, running isolated guest OSs.",
        "weight": 1
    },
    {
        "id": "devops_vm_002",
        "domain": "cloud_devops",
        "skill": "Virtual Machines",
        "difficulty": "medium",
        "question": "What is the core structural difference between Type 1 (bare-metal) and Type 2 (hosted) hypervisors?",
        "options": [
            {"id": "A", "text": "Type 1 hypervisors run directly on host hardware for high performance; Type 2 hypervisors run as applications on top of an existing host operating system."},
            {"id": "B", "text": "Type 1 is only for Linux; Type 2 is only for Windows VMs."},
            {"id": "C", "text": "Type 2 hypervisors do not support network routing."},
            {"id": "D", "text": "Type 1 requires GPUs to function, whereas Type 2 does not."}
        ],
        "correct_option_id": "A",
        "explanation": "Type 1 (ESXi, Xen) runs directly on the hardware, maximizing virtualization efficiency. Type 2 (VirtualBox, VMware Workstation) runs within an OS, suffering from host OS translation overhead.",
        "weight": 1
    },
    {
        "id": "devops_vm_003",
        "domain": "cloud_devops",
        "skill": "Virtual Machines",
        "difficulty": "hard",
        "question": "Compare the architecture and startup overhead of Virtual Machines versus Containers regarding guest OS inclusion.",
        "options": [
            {"id": "A", "text": "Virtual machines share the host kernel directly; containers require loading full kernel images."},
            {"id": "B", "text": "Virtual Machines include a full guest Operating System, kernel, and virtual drivers, resulting in gigabyte footprints and minutes to start; Containers share the host OS kernel and isolate user space, resulting in megabyte footprints and milliseconds to start."},
            {"id": "C", "text": "Containers require virtual BIOS booting; VMs run directly in namespaces."},
            {"id": "D", "text": "Both use identical virtual kernels, leading to identical startup times."}
        ],
        "correct_option_id": "B",
        "explanation": "VMs simulate complete systems, loading distinct guest kernels, which takes time and memory. Containers are lightweight isolated processes running directly on the host kernel, starting near-instantaneously.",
        "weight": 1
    },

    # Kubernetes Basics
    {
        "id": "devops_k8s_001",
        "domain": "cloud_devops",
        "skill": "Kubernetes Basics",
        "difficulty": "easy",
        "question": "What is the smallest deployable object in Kubernetes architecture?",
        "options": [
            {"id": "A", "text": "Container"},
            {"id": "B", "text": "Pod"},
            {"id": "C", "text": "Service"},
            {"id": "D", "text": "Deployment"}
        ],
        "correct_option_id": "B",
        "explanation": "A Pod represents a single instance of a running process in your cluster, hosting one or more tightly coupled containers sharing network and storage namespace.",
        "weight": 1
    },
    {
        "id": "devops_k8s_002",
        "domain": "cloud_devops",
        "skill": "Kubernetes Basics",
        "difficulty": "medium",
        "question": "What is the difference between a Pod and a Service in Kubernetes?",
        "options": [
            {"id": "A", "text": "Pods compile images, while Services deploy them."},
            {"id": "B", "text": "A Pod is a transient running container group; a Service is a stable network endpoint that exposes a logical set of Pods, routing traffic dynamically as Pods terminate or scale."},
            {"id": "C", "text": "Services run only on worker nodes; Pods run on master nodes."},
            {"id": "D", "text": "Pods are databases; Services are API routes."}
        ],
        "correct_option_id": "B",
        "explanation": "Pods are ephemeral. When they die, their IPs change. A Service defines a policy-driven abstraction layer (stable IP/DNS) over dynamic Pod targets.",
        "weight": 1
    },
    {
        "id": "devops_k8s_003",
        "domain": "cloud_devops",
        "skill": "Kubernetes Basics",
        "difficulty": "hard",
        "question": "Explain the role and communication flow of the Kubernetes Control Plane components: API Server, etcd, Scheduler, and Controller Manager.",
        "options": [
            {"id": "A", "text": "etcd compiles code; scheduler builds images; API server routes requests; controller manager allocates ports."},
            {"id": "B", "text": "The API Server is the entrypoint for all cluster commands; etcd is the key-value database storing cluster state; the Scheduler assigns Pods to nodes; the Controller Manager runs loop regulators to maintain the desired cluster state (replicas, node status)."},
            {"id": "C", "text": "API Server runs on Docker; etcd runs on PostgreSQL; Scheduler coordinates database queries."},
            {"id": "D", "text": "The control plane runs strictly in worker nodes, bypassing etcd."}
        ],
        "correct_option_id": "B",
        "explanation": "The API Server is the central communications hub. It writes state to etcd. The scheduler watches for unassigned Pods and schedules them to nodes. The controller manager runs reconcile loops, comparing active states to target layouts.",
        "weight": 1
    },

    # Cloud Security
    {
        "id": "devops_sec_001",
        "domain": "cloud_devops",
        "skill": "Cloud Security",
        "difficulty": "easy",
        "question": "Which security principle enforces granting users only the minimum access permissions necessary to perform their job duties?",
        "options": [
            {"id": "A", "text": "Security through obscurity"},
            {"id": "B", "text": "Principle of Least Privilege"},
            {"id": "C", "text": "Single Sign-On (SSO)"},
            {"id": "D", "text": "Defense in Depth"}
        ],
        "correct_option_id": "B",
        "explanation": "The Principle of Least Privilege (PoLP) minimizes access rights, limiting potential damage from compromised credentials.",
        "weight": 1
    },
    {
        "id": "devops_sec_002",
        "domain": "cloud_devops",
        "skill": "Cloud Security",
        "difficulty": "medium",
        "question": "What is the difference between IAM Users and IAM Roles in cloud environments (like AWS)?",
        "options": [
            {"id": "A", "text": "Users represent databases, while Roles represent policies."},
            {"id": "B", "text": "An IAM User represents a permanent identity (with long-term credentials); an IAM Role is assumed temporarily by users or applications, providing temporary, auto-rotating security credentials."},
            {"id": "C", "text": "Roles are only for billing, whereas Users handle API connections."},
            {"id": "D", "text": "IAM Users are hosted on-premises; IAM Roles are hosted in the cloud."}
        ],
        "correct_option_id": "B",
        "explanation": "IAM Users have permanent keys, which pose leakage risks. IAM Roles are assumed on-demand (e.g. by EC2 services or users), yielding short-lived STS tokens, mitigating security exposures.",
        "weight": 1
    },
    {
        "id": "devops_sec_003",
        "domain": "cloud_devops",
        "skill": "Cloud Security",
        "difficulty": "hard",
        "question": "Describe the concept of 'Zero Trust Architecture' in cloud environments and how it differs from traditional perimeter-based security.",
        "options": [
            {"id": "A", "text": "Zero Trust assumes all developers are malicious and blocks Git access entirely."},
            {"id": "B", "text": "Traditional security trusts anything inside the corporate network perimeter (firewall); Zero Trust assumes threats exist everywhere, requiring continuous verification, micro-segmentation, and strict access controls for every request regardless of origin."},
            {"id": "C", "text": "Zero Trust relies entirely on physical hardware keys, removing all digital firewalls."},
            {"id": "D", "text": "Zero Trust is a policy that stops all incoming REST API queries."}
        ],
        "correct_option_id": "B",
        "explanation": "Zero Trust is 'never trust, always verify'. Perimeter security (castle-and-moat) is vulnerable if an intruder gains internal entry. Zero Trust enforces strict identity verification, device health checks, and context authentication at every API call layer.",
        "weight": 1
    }
]

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    generate_domain_file(os.path.join(base_dir, 'machine_learning.json'), ml_questions)
    generate_domain_file(os.path.join(base_dir, 'data_science.json'), ds_questions)
    generate_domain_file(os.path.join(base_dir, 'generative_ai.json'), genai_questions)
    generate_domain_file(os.path.join(base_dir, 'web_development.json'), web_questions)
    generate_domain_file(os.path.join(base_dir, 'cloud_devops.json'), devops_questions)
