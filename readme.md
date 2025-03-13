# Ανάπτυξη Εφαρμογής Εξατομικευμένης Διατροφής με Χρήση Μεγάλου Γλωσσικού Μοντέλου (LLM)
### Περιγραφή
Ο σκοπός της πτυχιακής εργασίας είναι η αξιοποίηση των LLM μοντέλων για την για την παραγωγή πληροφοριών καθοδηγώντας τα δεδομένα που εισάγει ο χρήστης ως prompt στο μοντέλο. Πιο συγκεκριμένα, αναπτύσσουμε μια εφαρμογή που θα κάνει χρήση ενός LLM μοντέλου για την παραγωγή εξειδικευμένων προγραμμάτων διατροφής, τα αποτελέσματα των οποίων εξαρτώνται από τις επιλογές που θα δώσει ο χρήστης. Η εφαρμογή διατίθεται διαδικτυακά ώστε ένας χρήστης ανεξαρτήτου εφαρμογής να μπορεί να έχει πρόσβαση. 
<br><br>Για την χρήση της εφαρμογής ο χρήστης μέσω συγκεκριμένης ιστοσελίδας θα φορτώνει μια φόρμα μέσω της οποίας μπορεί να εισάγει προσωπικές πληροφορίες που σχετίζονται με τις διατροφικές του συνήθειες, όπως φύλο, ηλικία, τύπος διατροφής, αλλεργίες και δυσανεξίες. Κατά την υποβολή της φόρμας, τα δεδομένα χρησιμοποιούνται για να συμπληρώσουν ένα προκαθορισμένο προσχέδιο prompt. Σκοπός του προσχεδίου είναι το prompt να προσαρμόζεται δυναμικά στα δεδομένα του χρήστη, ώστε το prompt να είναι κατανοητό ακόμα κι αν ο χρήστης παραλείψει να εισάγει ορισμένες πληροφορίες. Στη συνέχει τα prompt δίνεται ως είσοδος στη συνάρτηση παραγωγής του μοντέλου.
<br><br>Για να μπορέσουμε να χρησιμοποιήσουμε τις παραγόμενες πληροφορίες των γευμάτων, μας βοηθά το αποτέλεσμα να ακολουθεί μια συγκεκριμένη δομή. Γι’ αυτό μέσω του prompt ζητάμε από το μοντέλο να αξιοποιήσει μια συγκεκριμένη δομή JSON και μέσα σε εκείνη να παράξει τις ζητούμενες πληροφορίες. Για να αποφύγουμε την παραγωγή περιττού κειμένου χρησιμοποιείται η Jsonformer, μια βιβλιοθήκη της python η οποία αναγκάζει τις απαντήσεις του μοντέλου να ακολουθεί αυστηρά τη JSON δομή. Είναι σημαντικό να περιορίσουμε την τυχαιότητα των απαντήσεων του μοντέλου, για να μπορέσουμε να αυτοματοποιήσουμε την εμφάνιση του αποτελέσματος στον χρήστη. Η παραγωγή των γευμάτων διαρκεί μερικά δευτερόλεπτα, ενώ όταν η απάντηση του μοντέλου ολοκληρωθεί, οι πληροφορίες κατανέμονται σε συγκεκριμένα μέρη μέσα στη σελίδα αποτελεσμάτων της ιστοσελίδας.
<br><br>Η python είναι η γλώσσα που επιλέχθηκε για την υλοποίηση, καθώς περιλαμβάνει πληθώρα βιβλιοθηκών για την φόρτωση και εκτέλεση γλωσσικών μοντέλων. Για την ανάπτυξη της διαδικτυακής εφαρμογής χρησιμοποιήθηκε το Flask, το οποίο είναι ένα Web Framework που ακολουθεί το πρωτόκολλο WSGI (Web Server Gateway Interface). Πιο αναλυτικά, αυτό που το Flask καταφέρνει μέσω του πρωτοκόλλου WSGI είναι να διαχειρίζεται HTTP αιτήματα του WSGI εξυπηρετητή, να τα μετατρέπει σε python συναρτήσεις, να τις εκτελεί και να επιστρέφει HTTP response. Κατά την εκτέλεση της flask εφαρμογής μας, ο χρήστης αποκτά πρόσβαση στην διαδικτυακή εφαρμογή μέσω μιας προκαθορισμένης θύρας. Όταν ο χρήστης στείλει ένα HTTP αίτημα, θα διαβιβαστεί στον WSGI server και στη συνέχεια θα μετατραπεί σε python κλήση, η οποία μπορεί να εκτελεστεί μέσω της flask εφαρμογής. Επιπλέον, το Flask χρησιμοποιεί τη βιβλιοθήκη Jinja2, η οποία επιτρέπει τη δυναμική δημιουργία HTML σε web εφαρμογές με την ενσωμάτωση μεταβλητών, συνθηκών, βρόχων και άλλων δυναμικών λειτουργιών μέσα στην HTML.
<br><br>Το flask από προεπιλογή εκτελείται τοπικά σε προκαθορισμένη θύρα (port). Για να εκθέσουμε την εφαρμογή σε κάποια δημόσια διεύθυνση αξιοποιούμε το Ngrok, το οποίο λειτουργεί ως ενδιάμεσος proxy, δρομολογώντας την κίνηση μεταξύ του διαδικτύου και του τοπικού server. Όταν εκτελούμε την εφαρμογή, το ngrok δημιουργεί ένα ασφαλές tunnel προς το διαδίκτυο και ένα τυχαίο https url.
<br><br>

### Ανάλυση Κώδικα
#### Το αντικείμενο app - app.py
```
app = Flask(__name__)
```
Δημιουργεί ένα στιγμιότυπο της κλάσης Flask και το εκχωρεί στο αντικείμενο <b>app</b>. Η παράμετρος <b>\_\_name\_\_</b> είναι σημαντική για την λειτουργία της flask εφαρμογής, διότι το Flask πρέπει να γνωρίζει από ποιο αρχείο εκτελείται η εφαρμογή, ώστε να μπορεί να βρει στατικά αρχεία, templates και να ρυθμίσει σωστά τις διαδρομές. Το αντικείμενο `a` χρησιμοποιείται στη συνέχεια για να ορίσουμε διαδρομές (routes), να ρυθμίσουμε παραμέτρους (settings) και να εκκινήσουμε τον διακομιστή (server).

<br>

#### Η συνάρτηση auth() - app.py
```
def auth():
    # Εξουσιοδότηση του ngrok με χρήση authentication token
    ngrok_auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    
    # Εκτέλεση εντολής για ρύθμιση του ngrok authentication token
    os.system(f'ngrok authtoken {ngrok_auth_token}')

    # Σύνδεση στο Hugging Face Hub για πρόσβαση στο μοντέλο
    login('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
```
    
Η συνάρτηση `auth()`:
- Εξουσιοδοτεί (Authenticate) το Ngrok, ώστε να μπορεί να δημιουργήσει δημόσια URL.
- Εξουσιοδοτεί το Hugging Face Hub ώστε να έχουμε πρόσβαση στο κλειστό (gated) αποθετήριο που είναι διαθέσιμο το μοντέλο Llama-2-7b-chat-hf. Η άδεια χρήσης του μοντέλου έχει δοθεί κατόπιν αιτήματος μέσω της ειδικής φόρμας στο Hugging Face.

Έχουμε δημιουργήσει Personal Access Tokens για την αυθεντικοποίηση των λογαριασμών που έχουν πρόσβαση στις παραπάνω υπηρεσίες.

<br>

#### Συνάρτηση before_request() - app.py
```
@app.before_request
def before_request():
    app.jinja_env.cache = None # Απενεργοποίηση της cache των templates
    app.jinja_env.auto_reload = True # Ενεργοποίηση αυτόματης ανανέωσης των template
    app.config['TEMPLATES_AUTO_RELOAD'] = True # Επιτρέπει την αυτόματη επαναφόρτωση των templates χωρίς restart
```
 Ο decorator της Flask @app.before_request εκτελεί τη συνάρτηση before_request() πριν από κάθε request. Χρησιμοποιείται για την εκτέλεση ενεργειών που πρέπει να γίνουν πριν από κάθε HTTP request, όπως έλεγχοι ή ρυθμίσεις.
 Η app.jinja_env.cache είναι η cache του Jinja2 (το template engine που χρησιμοποιεί η Flask. Θέτοντας την τιμή σε None, απενεργοποιούμε την cache, επιτρέποντας στα templates να φορτώνονται ξανά σε κάθε request και είναι χρήσιμο κατά την ανάπτυξη της εφαρμογής.
 Όταν θέτουμε το app.jinja_env.auto_reload την τιμή True, το Flask παρακολουθεί αλλαγές στα αρχεία των templates και τα ανανεώνει αυτόματα. Χωρίς αυτήν τη ρύθμιση, οι αλλαγές στα HTML αρχεία των templates δεν θα φαίνονται μέχρι να γίνει restart της εφαρμογής.

<br>

#### Συνάρτηση index() - app.py
```
@app.route("/", methods=["GET"])
def index():
     return render_template("index.html", 
                            genders=Constants.GENDERS, 
                            activityLevels=Constants.ACTIVITY_LEVELS, 
                            healthGoals=Constants.HEALTH_GOALS, 
                            dietaryTypes=Constants.DIETARY_TYPES, 
                            foodAllergies=Constants.FOOD_ALLERGIES, 
                            foodIntolerancies=Constants.FOOD_INTOLERANCHES, 
                            micronutrientFocus=Constants.MICRONUTRIENT_FOCUS,
                            cookingDifficulty=Constants.COOKING_DIFFICULTY)
```
Η συνάρτηση index() είναι μια route function σε μια Flask εφαρμογή. Ο ρόλος της είναι να χειρίζεται αιτήματα προς την αρχική σελίδα (/) και να επιστρέφει το αρχείο HTML template index.html μέσω της συνάρτησης `render_template()`. Η `render_template()` λαμβάνει ως παραμέτρους το όνομα του HTML αρχείου της αρχικής μας σελίδας και επιπλέον μια σειρά από σταθερές που έχουμε ορίσει στο αρχειο `Constants.py`. Οι σταθερές αυτές συγκρατούν πληροφορίες όπως dropdown list τιμές που χρησιμοποιούνται από τα δυναμικά templates που υπάρχουν μέσα στην `index.html`.

<br>

#### Συνάρτηση getSubmitForm() - app.py
```
@app.route('/submit', methods=['POST'])
def getSubmitForm():
    try:
        # Λήψη δεδομένων που εισήγαγε ο χρήστης
        gender = request.form.get("gender")
        age = request.form.get("age")
        diet_type = request.form.get("diet_type")
        goals = request.form.getlist("goals")  # Get list of selected goals
        allergies = request.form.getlist("allergies")  # Get list of selected allergies
        intolerances = request.form.getlist("intolerances")  # Get list of selected intolerances

        # Εμφάνιση Δεδομένων χρήστη
        print('Data retrived from user\n');
        print('Gender: '+gender);
        print('diet_type: '+diet_type);
        print('goals: '+str(goals));
        print('intolerances: '+str(intolerances));
        print('intolerances: '+str(intolerances));

        # Προκαθορισμένη JSON δομή απαντήσεων για τροφοδοσία του Jsonformer
        json_schema = {
            "title": "MealPlan",
            "type": "object",
            "properties": {
                "breakfast": {
                    "type": "object",
                    "properties": {
                        "mealName": {"type": "string"},
                        "ingredients": {"type": "array", "items": {"type": "string"}},
                        "instructions": {"type": "string",
                                         "minLength": 200,
                                         "maxLength": 300
                                         },
                        "cookingTime": {"type": "number"},
                        "calories": {"type": "number"},
                        "macros": {
                            "type": "object",
                            "properties": {
                                "protein": {"type": "number"},
                                "carbs": {"type": "number"},
                                "fat": {"type": "number"},
                            },
                        },
                    },
                },
                "lunch": {
                    "type": "object",
                    "properties": {
                        "mealName": {"type": "string"},
                        "ingredients": {"type": "array", "items": {"type": "string"}},
                        "instructions": {"type": "string",
                                         "minLength": 200,
                                         "maxLength": 300
                                         },
                        "cookingTime": {"type": "number"},
                        "calories": {"type": "number"},
                        "macros": {
                            "type": "object",
                            "properties": {
                                "protein": {"type": "number"},
                                "carbs": {"type": "number"},
                                "fat": {"type": "number"},
                            },
                        },
                    },
                },
                "dinner": {
                    "type": "object",
                    "properties": {
                        "mealName": {"type": "string"},
                        "ingredients": {"type": "array", "items": {"type": "string"}},
                        "instructions": {"type": "string",
                                         "minLength": 200,
                                         "maxLength": 300
                                         },
                        "cookingTime": {"type": "number"},
                        "calories": {"type": "number"},
                        "macros": {
                            "type": "object",
                            "properties": {
                                "protein": {"type": "number"},
                                "carbs": {"type": "number"},
                                "fat": {"type": "number"},
                            },
                        },
                    },
                },
            },
        }

        # Προσχέδιο προτροπής
        prompt = f"""
            You are a meal planner that provides to users a day meal plan in the form of json.
            The user's gender is {gender} and is {age} years old.
            The user follows {'a '+diet_type if diet_type else 'any'} diet and has the following goals: {goals if goals else 'None'}.
            The user is allergic to {allergies if allergies else 'nothing'}.
            The user is food intolerant to {intolerances if intolerances else 'nothing'}.

            Please generate a JSON object following this structure:
            - "breakfast": Contains details of the breakfast meal.
              - "mealName": A descriptive name of the meal.
              - "ingredients": A list of ingredients required.
              - "instructions": Step-by-step instructions for preparation using minimum 150 characters
              - "cookingTime": Time required to prepare the meal in minutes.
              - "calories": Total calorie count for the meal.
              - "macros": A breakdown of macronutrients.
                - "protein": Amount of protein in grams.
                - "carbs": Amount of carbohydrates in grams.
                - "fat": Amount of fat in grams.

            - "lunch": Similar structure to breakfast.
            - "dinner": Similar structure to breakfast.

            The meal names should be realistic, ingredients should be commonly available, cookingTime must correspond to the time needed for cooking the meal  and macros should be reasonable. Ensure the JSON output follows the expected structure exactly without extra text."""

        # Εμφάνιση προτροπής
        print('Prompt used: '+prompt);
        
        # Δημιουργία αντικειμένου Jsonformer για παραγωγή δομημένης JSON εξόδου από το γλωσσικό μοντέλο
        jsonformer = Jsonformer(model, tokenizer, json_schema, prompt, max_string_token_length=3000)

        # Κλήση του Jsonformer για τη δημιουργία JSON δεδομένων σύμφωνα με το καθορισμένο σχήμα
        response = jsonformer()

        # Εμφάνιση παραγόμενου αποτελέσματος
        print(response)

        # Φόρτωση της σελίδας αποτελεσμάτων
        return render_template("results.html", results=response)

    # Διαχείριση σφαλμάτων με τη φόρτωση σελίδας σφάλματος
    except Exception as e:
        print(e)
        return render_template("error.html", error={"error": str(e)}) #return render_template("results.html", response=jsonify({"response": response}))

```
- @app.route('/submit', methods=['POST']): Ορίζει μια διαδρομή (/submit) που δέχεται μόνο POST αιτήματα.
- def getSubmitForm(): Δημιουργεί τη συνάρτηση getSubmitForm() που θα εκτελείται όταν ο χρήστης υποβάλλει δεδομένα στη φόρμα.

```
gender = request.form.get("gender")
age = request.form.get("age")
diet_type = request.form.get("diet_type")
goals = request.form.getlist("goals")
allergies = request.form.getlist("allergies")
intolerances = request.form.getlist("intolerances")
```
Χρησιμοποιεί request.form.get() και request.form.getlist() για να λάβει δεδομένα που έχουν υποβληθεί από τη φόρμα. Το getlist() χρησιμοποιείται για πεδία που περιέχουν πολλαπλές επιλογές (π.χ. λίστα αλλεργιών).

```
json_schema = {
    "title": "MealPlan",
    "type": "object",
    "properties": {
        "breakfast": {
            "type": "object",
            "properties": {
                "mealName": {"type": "string"},
                "ingredients": {"type": "array", "items": {"type": "string"}},
                "instructions": {"type": "string", "minLength": 200, "maxLength": 300},
                "cookingTime": {"type": "number"},
                "calories": {"type": "number"},
                "macros": {
                    "type": "object",
                    "properties": {
                        "protein": {"type": "number"},
                        "carbs": {"type": "number"},
                        "fat": {"type": "number"},
                    },
                },
            },
        },
        ...
    },
}
```
Δημιουργεί μια JSON δομή (schema) που καθορίζει το φορμάτ των δεδομένων που θα δημιουργήσει το μοντέλο. Ορίζει τις ιδιότητες (properties) κάθε γεύματος (πρωινό, μεσημεριανό, βραδινό), συμπεριλαμβάνοντας:
- mealName: Όνομα του γεύματος
- ingredients: Λίστα με συστατικά
- instructions: Οδηγίες παρασκευής με ελάχιστο μήκος χαρακτήρων
- cookingTime: Χρόνος μαγειρέματος
- calories: Συνολικές θερμίδες
- macros: Ανάλυση μακροθρεπτικών συστατικών (πρωτεΐνες, υδατάνθρακες, λίπη)

```
prompt = f"""
            You are a meal planner that provides to users a day meal plan in the form of json.
            The user's gender is {gender} and is {age} years old.
            The user follows {'a '+diet_type if diet_type else 'any'} diet and has the following goals: {goals if goals else 'None'}.
            The user is allergic to {allergies if allergies else 'nothing'}.
            The user is food intolerant to {intolerances if intolerances else 'nothing'}.

            Please generate a JSON object following this structure:
            - "breakfast": Contains details of the breakfast meal.
              - "mealName": A descriptive name of the meal.
              - "ingredients": A list of ingredients required.
              - "instructions": Step-by-step instructions for preparation using minimum 150 characters
              - "cookingTime": Time required to prepare the meal in minutes.
              - "calories": Total calorie count for the meal.
              - "macros": A breakdown of macronutrients.
                - "protein": Amount of protein in grams.
                - "carbs": Amount of carbohydrates in grams.
                - "fat": Amount of fat in grams.

            - "lunch": Similar structure to breakfast.
            - "dinner": Similar structure to breakfast.

            The meal names should be realistic, ingredients should be commonly available, cookingTime must correspond to the time needed for cooking the meal  and macros should be reasonable. Ensure the JSON output follows the expected structure exactly without extra text."""
"""
```
Δημιουργεί ένα prompt για το γλωσσικό μοντέλο, καθορίζοντας τι πρέπει να περιλαμβάνει ή να αποφύγει στη δημιουργία των γευμάτων, λαμβάνοντας υπόψιν εξατομικευέμνες πληροφορίες για τον χρήστη (π.χ. φύλο, ηλικία, δίαιτα, αλλεργίες). Ζητάει από το μοντέλο να παράγει JSON αντικείμενο με συγκεκριμένη μορφή (σύμφωνα με το json_schema), το οποίο είναι εύχρηστο ως προς την αυτοματοποιημένη εμφάνιση των αποτελεσμάτων με ελεγχόμενο και δομημένο τρόπο.

```
jsonformer = Jsonformer(model, tokenizer, json_schema, prompt, max_string_token_length=3000)
response = jsonformer()
```
Αρχικοποιεί το αντικείμενο jsonformer, που αποτελεί στιγμιότυπο της κλάσης Jsonformer. Το Jsonformer είναι module της python που επιβάλει στα LLM μοντέλα να παράγουν αποτελέσματα σύμφωνα με προκαθορισμένα JSON σχήματα. Οι παράμετροι που δίνονται είναι οι εξής:
- model: Το γλωσσικό μοντέλο (LLM)
- tokenizer: Το tokenizer του μοντέλου
- json_schema: Το επιθυμητό JSON σχήμα
- prompt: Την προτροπή που ζητά την παραγωγή δεδομένων

<br>

#### Main - app.py
```
if __name__ == '__main__':
    auth()
```
Το πρώτο που πρέπει να εκτελεστεί είναι η Αυθεντικοποίηση για την χρήση Ngrok και HuggingFace, ώστε να έχουμε πρόσβαση στο μοντέλο και την δημιουργία δημόσιων συνδέσμων όπου η εφαρμογή μας θα τρέχει αντίστοιχα.
```
save_path = '/content/Saved Models/Llama-2-7b-chat-hf'
if os.path.exists(save_path):
    model = LlamaForCausalLM.from_pretrained(save_path)
    tokenizer = LlamaTokenizer.from_pretrained(save_path)
else:
    # Load model from hugging face
    model_id = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = LlamaTokenizer.from_pretrained(model_id, use_fast=True)
    model = LlamaForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_8bit=True
    )
os.makedirs(save_path, exist_ok=True)
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
```
Εν μέσω της ανάπτυξης της εφαρμογής εξοικονομούμε χρόνο και πόρους εάν αποθηκεύσουμε το μοντέλο τοπικά και το φορτώνουμε από τον τοπικό μας δίσκο. Διαφορετικά, η εφαρμογή κατεβάζει το μοντέλο από το Hugging Face.

```
if tokenizer.pad_token is None:
  tokenizer.pad_token = tokenizer.eos_token
```
Σε ορισμένα tokenizer (ιδιαίτερα στα μοντέλα Transformer), το pad token (tokenizer.pad_token) δεν είναι πάντα προκαθορισμένο. Το pad_token υποδηλώνει το τέλος μιας πρότασης ή ακολουθίας και χρησιμοποιείται για να γεμίσει ακολουθίες (padding), ώστε να έχουν το ίδιο μήκος. Αν το pad_token είναι None, τότε το μοντέλο μπορεί να μη χειρίζεται σωστά το padding. Αντί να αφήσουμε το pad_token άδειο, το ρυθμίζουμε να έχει την τιμή του eos_token, που υπάρχει στα περισσότερα μοντέλα.
    
```
public_url = ngrok.connect(5000).public_url
print(f"Public URL: {public_url}")
```
Καλεί τη συνάρτηση ngrok.connect(5000), η οποία δημιουργεί ένα δημόσιο URL χρησιμοποιώντας την υπηρεσία ngrok. Το 5000 είναι η πόρτα στην οποία εκτελείται η Flask εφαρμογή. Το .public_url επιστρέφει το URL που δημιουργήθηκε, ώστε να είναι δυνατή η πρόσβαση στην εφαρμογή Flask από το διαδίκτυο.
```
```
app.run()
```
Εκκινεί τη Flask εφαρμογή.
<br><br>

#### templates
#### static
#### Constants 
Ορίζουμε μια σελίδα (/): Με @app.route('/'), καθορίζουμε τι θα εμφανιστεί όταν κάποιος επισκεφτεί τη σελίδα.

![Εικόνα 1: Φόρμα εισαγωγής παραμέτρων](https://github.com/user-attachments/assets/6c3cf485-cfaa-4c5d-bee0-bf4e3b4d15ca)
<br><i>Εικόνα 1: Φόρμα εισαγωγής παραμέτρων</i><br><br>
![Εικόνα 2: Οθόνη κατά την παραγωγή απάντησης](https://github.com/user-attachments/assets/a380dc6c-3ee0-4754-a2bc-8c8287d64ed0)
<br><i>Εικόνα 2: Οθόνη κατά την παραγωγή απάντησης</i><br><br>
![Εικόνα 3: Οθόνη αποτελέσματος](https://github.com/user-attachments/assets/913df292-e921-4bcd-8e5c-4001dbde0425)
<br><i>Εικόνα 3: Οθόνη αποτελέσματος</i><br><br>
![Εικόνα 4: Το app.py παράγει την διεύθυνση στην οποία διατίθεται η εφαρμογή](https://github.com/user-attachments/assets/bbd592e2-c1a1-4bfe-ae8e-311e09b60cc2)
<br><i>Εικόνα 4: Το app.py παράγει την διεύθυνση στην οποία διατίθεται η εφαρμογή</i><br><br>


### Δομή Αποθετηρίου
<pre>
📂 app
├── 📂 static
│   ├── 📄 script.js
│   ├── 📄 style-results.css
│   ├── 📄 styles.css
├── 📂 templates
│   ├── 📄 error.html
│   ├── 📄 index.html
│   ├── 📄 results.html
├── 📄 Constants.py
├── 📄 ConstantsStaticMethods.py
├── 📄 app-mock-response.py
├── 📄 app.py
├── 📄 Nutrition_App_Thesis_Alexandra_Paramytha.ipynb
├── 📄 README.md
├── 📄 requirements.txt
</pre>

<br><br>

### Documentation
- Flask: https://flask.palletsprojects.com/en/stable/tutorial/
- Ngrok: https://ngrok.com/docs/guides/developer-preview/getting-started/
- Jsonformer: https://python.langchain.com/docs/integrations/llms/jsonformer_experimental/
- Llama 2 model: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
  
