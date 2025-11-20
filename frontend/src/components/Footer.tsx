import { Github, Linkedin, Mail } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h4 className="font-semibold mb-3">About BookReview</h4>
            <p className="text-gray-400 text-sm leading-relaxed">
              BookReview is a community-driven platform for discovering, 
              reviewing, and sharing your favorite books with fellow book enthusiasts 
              around the world.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-3">Quick Links</h4>
            <ul className="text-gray-400 text-sm space-y-2">
              <li className="hover:text-white cursor-pointer transition">
                Browse Books
              </li>
              <li className="hover:text-white cursor-pointer transition">
                My Reviews
              </li>
              <li className="hover:text-white cursor-pointer transition">
                Privacy Policy
              </li>
              <li className="hover:text-white cursor-pointer transition">
                Terms of Service
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-3">Suggest a Book</h4>
            <p className="text-gray-400 text-sm mb-3">
              Have a book recommendation? We'd love to hear about it!
            </p>
            <button className="w-full px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition text-sm font-medium">
              Submit Suggestion
            </button>
          </div>
        </div>

        <div className="border-t border-gray-700 pt-8">
          <div className="flex justify-between items-center flex-wrap gap-4">
            <div>
              <p className="text-gray-400 text-sm">
                &copy; 2024 BookReview Platform. All rights reserved.
              </p>
              <p className="text-gray-500 text-xs mt-2">
                Made with ❤️ by Selvam
              </p>
            </div>

            <div className="flex gap-4">
              <a
                href="mailto:selvam.mdg@gmail.com"
                className="text-gray-400 hover:text-white transition p-2 hover:bg-gray-800 rounded"
                title="Email"
              >
                <Mail size={20} />
              </a>
              <a
                href="https://linkedin.com/in/selvam"
                className="text-gray-400 hover:text-white transition p-2 hover:bg-gray-800 rounded"
                title="LinkedIn"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Linkedin size={20} />
              </a>
              <a
                href="https://github.com/selvamdg"
                className="text-gray-400 hover:text-white transition p-2 hover:bg-gray-800 rounded"
                title="GitHub"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github size={20} />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}