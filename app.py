import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the trained model
with open('decision.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML template with modern Tailwind CSS styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Placement Prediction Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gradient-to-br from-indigo-50 via-blue-50 to-slate-100 min-h-screen py-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-10">
            <div class="inline-flex items-center justify-center bg-indigo-600 text-white rounded-full p-3 shadow-lg mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
            </div>
            <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Campus Placement Predictor</h1>
            <p class="mt-2 text-lg text-slate-600">Enter academic and professional details to evaluate placement eligibility.</p>
        </div>

        <!-- Main Card -->
        <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
            <form action="/" method="POST" class="p-8 sm:p-10 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    <!-- Gender -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Gender</label>
                        <select name="gender" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                            <option value="1">Male</option>
                            <option value="0">Female</option>
                        </select>
                    </div>

                    <!-- Work Experience -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Work Experience</label>
                        <select name="workex" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                            <option value="1">Yes</option>
                            <option value="0">No</option>
                        </select>
                    </div>

                    <!-- SSC Percentage -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Secondary Education (SSC) %</label>
                        <input type="number" step="0.01" name="ssc_p" required placeholder="e.g. 67.0" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                    </div>

                    <!-- SSC Board -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">SSC Board</label>
                        <select name="ssc_b" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                            <option value="1">Central</option>
                            <option value="0">Others</option>
                        </select>
                    </div>

                    <!-- HSC Percentage -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Higher Secondary (HSC) %</label>
                        <input type="number" step="0.01" name="hsc_p" required placeholder="e.g. 75.5" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                    </div>

                    <!-- HSC Board -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">HSC Board</label>
                        <select name="hsc_b" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                            <option value="1">Central</option>
                            <option value="0">Others</option>
                        </select>
                    </div>

                    <!-- HSC Specialisation -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">HSC Stream</label>
                        <select name="hsc_s" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                            <option value="1">Commerce</option>
                            <option value="0">Science</option>
                            <option value="2">Arts</option>
                        </select>
                    </div>

                    <!-- Degree Percentage -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Degree Percentage</label>
                        <input type="number" step="0.01" name="degree_p" required placeholder="e.g. 65.0" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                    </div>

                    <!-- Degree Type -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Degree Type</label>
                        <select name="degree_t" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                            <option value="1">Comm&Mgmt</option>
                            <option value="0">Sci&Tech</option>
                            <option value="2">Others</option>
                        </select>
                    </div>

                    <!-- Etest Percentage -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Employability Test (Etest) %</label>
                        <input type="number" step="0.01" name="etest_p" required placeholder="e.g. 70.0" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                    </div>

                    <!-- MBA Specialisation -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">MBA Specialisation</label>
                        <select name="specialisation" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                            <option value="0">Mkt&Fin</option>
                            <option value="1">Mkt&HR</option>
                        </select>
                    </div>

                    <!-- MBA Percentage -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">MBA Percentage</label>
                        <input type="number" step="0.01" name="mba_p" required placeholder="e.g. 58.8" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50">
                    </div>

                </div>

                <!-- Submit Button -->
                <div class="pt-4">
                    <button type="submit" class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-indigo-500/30 transition duration-200 text-lg cursor-pointer">
                        Predict Placement Status
                    </button>
                </div>
            </form>

            {% if prediction_text is not none %}
            <!-- Result Box -->
            <div class="p-6 bg-slate-50 border-t border-slate-100 text-center">
                <div class="inline-block px-6 py-4 rounded-2xl {{ 'bg-emerald-100 text-emerald-800 border border-emerald-200' if prediction_text == 1 else 'bg-rose-100 text-rose-800 border border-rose-200' }} shadow-sm">
                    <h3 class="text-xl font-bold">
                        {{ '🎉 Congratulations! Candidate is likely to be PLACED.' if prediction_text == 1 else '⚠️ Candidate is unlikely to be placed based on current parameters.' }}
                    </h3>
                </div>
            </div>
            {% endif %}
        </div>

        <!-- Footer -->
        <div class="text-center mt-6 text-sm text-slate-500">
            Powered by Flask & Render
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    if request.method == 'POST':
        try:
            # Feature order extracted from decision.pkl:
            # ['gender', 'ssc_p', 'ssc_b', 'hsc_p', 'hsc_b', 'hsc_s', 'degree_p', 'degree_t', 'workex', 'etest_p', 'specialisation', 'mba_p']
            gender = int(request.form['gender'])
            ssc_p = float(request.form['ssc_p'])
            ssc_b = int(request.form['ssc_b'])
            hsc_p = float(request.form['hsc_p'])
            hsc_b = int(request.form['hsc_b'])
            hsc_s = int(request.form['hsc_s'])
            degree_p = float(request.form['degree_p'])
            degree_t = int(request.form['degree_t'])
            workex = int(request.form['workex'])
            etest_p = float(request.form['etest_p'])
            specialisation = int(request.form['specialisation'])
            mba_p = float(request.form['mba_p'])

            features = np.array([[gender, ssc_p, ssc_b, hsc_p, hsc_b, hsc_s, degree_p, degree_t, workex, etest_p, specialisation, mba_p]])
            
            prediction = model.predict(features)[0]
            prediction_text = int(prediction)
        except Exception as e:
            print(f"Error during prediction: {e}")
            prediction_text = None

    return render_template_string(HTML_TEMPLATE, prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True, port=5001)