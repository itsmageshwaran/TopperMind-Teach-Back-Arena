"""Seed notes and ideal answers. Keep the facts concise and reviewable."""
from config import COLLECTIONS

NOTES = {
 "UPSC Polity": [
  ("polity_art14", "Article 14 guarantees equality before the law and equal protection of the laws to every person in India. It permits reasonable classification, but classification must have an intelligible differentia and rational connection to its objective."),
  ("polity_art19", "Article 19(1) gives citizens six freedoms: speech and expression, peaceful assembly, association or unions, movement, residence, and profession or occupation. These freedoms are subject to reasonable restrictions specified in clauses 19(2) to 19(6)."),
  ("polity_art21", "Article 21 says no person shall be deprived of life or personal liberty except according to procedure established by law. The Supreme Court has interpreted life to include living with dignity."),
  ("polity_art32", "Article 32 guarantees the right to move the Supreme Court to enforce Fundamental Rights. The Court may issue habeas corpus, mandamus, prohibition, quo warranto, and certiorari."),
  ("polity_dpsp", "Directive Principles of State Policy are in Part IV, Articles 36–51. They are not enforceable by courts, but Article 37 says they are fundamental in governance and the State should apply them in making laws."),
  ("polity_fundamental_duties", "Fundamental Duties are listed in Article 51A, Part IVA. The 42nd Amendment Act, 1976 added ten duties; the 86th Amendment Act, 2002 added the duty concerning education for children aged six to fourteen."),
  ("polity_parliament", "The Parliament of India consists of the President, the Rajya Sabha, and the Lok Sabha under Article 79. A bill generally becomes law after passage by both Houses, where required, and the President's assent."),
  ("polity_money_bill", "Article 110 defines a Money Bill. It can be introduced only in the Lok Sabha on the President's recommendation. The Speaker certifies whether a bill is a Money Bill; the Rajya Sabha may recommend changes within 14 days."),
  ("polity_president", "The President of India is elected indirectly by an electoral college under Articles 54 and 55. The President ordinarily acts on the aid and advice of the Council of Ministers under Article 74."),
  ("polity_federalism", "The Seventh Schedule distributes legislative subjects among the Union List, State List, and Concurrent List. Parliament and State Legislatures can legislate on Concurrent List subjects, with Article 254 addressing repugnancy."),
  ("polity_emergency", "Article 352 provides for a Proclamation of Emergency when the security of India or a part is threatened by war, external aggression, or armed rebellion. Parliamentary approval and time limits are set by the Constitution."),
  ("polity_amendment", "Article 368 sets out Parliament's constituent power to amend the Constitution. Some amendments require a special majority, and amendments affecting specified federal provisions also require ratification by at least half of State Legislatures."),
 ],
 "College CS (DSA + DBMS)": [
  ("cs_stack", "A stack is a linear abstract data type that follows LIFO (last in, first out). Push adds an item to the top, pop removes the top item, and peek reads it. These operations are O(1) with an array or linked-list implementation."),
  ("cs_queue", "A queue follows FIFO (first in, first out): enqueue adds at the rear and dequeue removes from the front. A circular array or linked list supports these operations in O(1)."),
  ("cs_array", "An array stores elements in contiguous indexed positions. Index access is O(1); searching an unsorted array is O(n); inserting or deleting in the middle is O(n) due to shifting."),
  ("cs_linked_list", "A singly linked list stores nodes containing data and a pointer to the next node. Head insertion is O(1), indexed access is O(n), and deleting a node is O(1) when its predecessor is already known."),
  ("cs_binary_search", "Binary search finds a target in a sorted sequence by repeatedly halving the search interval. Its time complexity is O(log n); iterative implementation uses O(1) extra space."),
  ("cs_merge_sort", "Merge sort divides a sequence, recursively sorts each half, and merges the sorted halves. Its time complexity is O(n log n) in best, average, and worst cases; standard array implementations use O(n) auxiliary space."),
  ("cs_bst", "A binary search tree orders keys so values in the left subtree are smaller and values in the right subtree are larger, according to its ordering rule. Search, insert, and delete take O(h), where h is tree height; a balanced tree has O(log n) height."),
  ("cs_hash", "A hash table maps keys to array indices using a hash function. Collisions can be handled by chaining or open addressing. Expected lookup is O(1) with a suitable hash function and controlled load factor; worst case is O(n)."),
  ("cs_primary_key", "A primary key uniquely identifies each row in a relational table and cannot contain NULL. A table has one primary key constraint, which may consist of one or more columns."),
  ("cs_foreign_key", "A foreign key is a column or set of columns whose values reference a candidate key, commonly a primary key, in another or the same table. It enforces referential integrity."),
  ("cs_normalization", "Normalization organizes relational tables to reduce redundancy and update anomalies. In 1NF, each field contains an atomic value and rows are identifiable. 2NF removes partial dependency on part of a composite candidate key."),
  ("cs_acid", "ACID describes transaction properties: Atomicity (all or nothing), Consistency (valid states), Isolation (concurrent transactions behave safely), and Durability (committed changes persist)."),
 ],
 "School Science (Class 10)": [
  ("sci_photosynthesis", "Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen. The balanced equation is 6CO2 + 6H2O → C6H12O6 + 6O2, in the presence of light and chlorophyll."),
  ("sci_respiration", "Aerobic cellular respiration releases energy by oxidizing glucose with oxygen: C6H12O6 + 6O2 → 6CO2 + 6H2O + energy. It occurs through several stages in cells."),
  ("sci_ohm", "Ohm's law states that, at constant physical conditions, potential difference V across a conductor equals current I times resistance R: V = IR. The SI unit of resistance is the ohm (Ω)."),
  ("sci_power", "Electrical power is the rate of electrical energy transfer. For a circuit element, P = VI; using Ohm's law, P = I²R and P = V²/R. Power is measured in watts."),
  ("sci_mirror", "For spherical mirrors, using the Cartesian sign convention, the mirror formula is 1/f = 1/v + 1/u, where f is focal length, v image distance, and u object distance. Magnification m = -v/u."),
  ("sci_lens", "For a thin lens with the Cartesian sign convention, 1/f = 1/v - 1/u, where f is focal length, v image distance, and u object distance. Magnification m = v/u."),
  ("sci_acids", "Acids produce hydrogen ions in aqueous solution; bases produce hydroxide ions in aqueous solution. The pH scale commonly runs from 0 to 14; pH below 7 is acidic, 7 is neutral, and above 7 is basic at room temperature."),
  ("sci_metals", "Metals generally conduct heat and electricity and are malleable and ductile. Metals react with oxygen to form metal oxides; many metal oxides are basic, though some are amphoteric."),
  ("sci_carbon", "Carbon has atomic number 6 and commonly forms four covalent bonds. Catenation, the ability to form carbon chains, and tetravalency help explain the large number of carbon compounds."),
  ("sci_reproduction", "In human sexual reproduction, the sperm and ovum fuse during fertilization to form a zygote. The zygote develops into an embryo; in humans, development occurs in the uterus."),
  ("sci_heredity", "Genes are units of heredity made of DNA and located on chromosomes. Traits can be influenced by inherited genetic information and, for some traits, environmental factors."),
  ("sci_foodchain", "A food chain shows transfer of food and energy between organisms. Producers capture energy, consumers obtain it by feeding, and decomposers break down dead matter. Energy available generally decreases at successive trophic levels."),
 ]
}

# Four approximately 60-word scoring anchors in each collection.
MODEL = {
 "College CS (DSA + DBMS)": {
  "Stack": "A stack is a linear abstract data type that follows LIFO: last in, first out. Push adds an item to the top, pop removes the top item, and peek reads the top without removing it. With an array or linked list, these operations take O(1) time. Stacks are useful for undo actions, function calls, and checking balanced brackets.",
  "Queue": "A queue is a linear abstract data type that follows FIFO: first in, first out. Enqueue adds an item at the rear, and dequeue removes an item from the front. A circular array or linked list can support both operations in O(1) time. Queues are useful for scheduling jobs, handling requests in arrival order, and breadth-first graph traversal.",
  "Binary Search": "Binary search finds a target in a sorted sequence by checking the middle item and discarding the half that cannot contain the target. It repeats until the target is found or no candidates remain. Its time complexity is O(log n), and an iterative version uses O(1) extra space. The input must be sorted under the same ordering used by the search.",
  "ACID": "ACID describes four properties that help database transactions remain reliable. Atomicity means all transaction steps happen or none do. Consistency preserves database rules. Isolation limits interference between concurrent transactions. Durability means committed changes survive failures. Together, these properties help prevent partial updates and protect data when multiple users or operations access a database at once.",
 },
 "UPSC Polity": {
  "Article 14": "Article 14 of the Constitution guarantees equality before the law and equal protection of the laws to every person in India. Equality does not always require identical treatment: the State may make a reasonable classification. Such a classification must rest on an intelligible differentia and that differentia must have a rational connection to the law's objective. Arbitrary discrimination is not permitted.",
  "Article 21": "Article 21 provides that no person shall be deprived of life or personal liberty except according to procedure established by law. It protects every person, not citizens alone. The Supreme Court has interpreted the right to life broadly to include living with dignity. Any restriction must therefore follow valid legal procedure and meet constitutional requirements.",
  "Fundamental Duties": "Fundamental Duties appear in Part IVA, Article 51A of the Constitution. The 42nd Amendment Act, 1976 added ten duties. The 86th Amendment Act, 2002 added a duty for a parent or guardian to provide educational opportunities to a child or ward aged six to fourteen years. Duties guide civic conduct, though they are generally not directly enforceable by courts.",
  "Money Bill": "Article 110 defines a Money Bill by its provisions, including matters such as taxation, government borrowing, and appropriation of money from the Consolidated Fund of India. It can be introduced only in the Lok Sabha on the President's recommendation. The Speaker certifies whether a bill is a Money Bill. The Rajya Sabha may recommend changes within 14 days, but the Lok Sabha may accept or reject them.",
 },
 "School Science (Class 10)": {
  "Photosynthesis": "Photosynthesis is the process by which green plants use light energy to make glucose from carbon dioxide and water. Chlorophyll captures light energy, and oxygen is released. The balanced equation is 6CO2 + 6H2O → C6H12O6 + 6O2, in the presence of light and chlorophyll. This process stores energy in food and supplies oxygen to the environment.",
  "Ohm's Law": "Ohm's law states that, when physical conditions such as temperature remain constant, the potential difference V across a conductor is proportional to the current I through it. The relationship is V = IR, where R is resistance, measured in ohms (Ω). If resistance stays constant, increasing voltage increases current proportionally. The law describes many metallic conductors under suitable conditions.",
  "Acids and Bases": "In aqueous solution, acids produce hydrogen ions and bases produce hydroxide ions. The pH scale commonly ranges from 0 to 14 at room temperature. A pH below 7 is acidic, 7 is neutral, and above 7 is basic. Indicators such as litmus can help identify acidic or basic solutions. The pH value relates to hydrogen-ion concentration.",
  "Food Chain": "A food chain shows how food and energy pass between organisms. Producers, such as green plants, make food using sunlight. Consumers obtain energy by eating plants or other animals, while decomposers break down dead matter and recycle nutrients. Energy available generally decreases at each higher trophic level because organisms use much of it for life processes and release heat.",
 }
}

FOLLOWUPS = {
 "Stack": "If we push A, then B, and pop once, what is on top and why?",
 "Queue": "If the first person to join a line leaves first, what rule is the queue following?",
 "Binary Search": "Why does binary search need the items to be sorted first?",
 "ACID": "If a transaction stops halfway, which ACID idea helps prevent a half-finished result?",
 "Article 14": "Does equality mean every person must always be treated identically?",
 "Article 21": "Who does Article 21 protect: citizens only, or every person?",
 "Fundamental Duties": "Can you name the Article where these duties are listed?",
 "Money Bill": "What can the Rajya Sabha do with a Money Bill, and how many days does it get?",
 "Photosynthesis": "Which gas goes into the process, and which gas comes out?",
 "Ohm's Law": "If resistance stays the same and voltage doubles, what happens to current?",
 "Acids and Bases": "What pH value is neutral in the usual school scale?",
 "Food Chain": "Why is less energy usually available higher up the food chain?",
}

def seed_database(client, embedding_function):
    collections = {}
    for display, name in COLLECTIONS.items():
        col = client.get_or_create_collection(name=name, embedding_function=embedding_function)
        if col.count() == 0:
            rows = NOTES[display]
            col.add(ids=[r[0] for r in rows], documents=[r[1] for r in rows], metadatas=[{"topic": r[0]} for r in rows])
        collections[display] = col
    return collections

