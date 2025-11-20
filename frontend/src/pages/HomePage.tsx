import { BookOpen, Star, Heart, Users, TrendingUp, Award } from "lucide-react";

interface HomePageProps {
  onBooksClick: () => void;
}

export default function HomePage({ onBooksClick }: HomePageProps) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-[calc(100vh-200px)]">
      {/* Hero Section */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-6 animate-bounce">
            <BookOpen size={64} className="text-indigo-600" />
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            Book Review Platform
          </h1>
          <p className="text-xl md:text-2xl text-gray-700 mb-8">
            Discover, review, and share your favorite books with a community of 
            passionate readers worldwide.
          </p>
          <button
            onClick={onBooksClick}
            className="px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition transform hover:scale-105"
          >
            Start Exploring Books
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
            Why Choose BookReview?
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition hover:-translate-y-2">
              <Star className="text-yellow-500 mb-3" size={36} />
              <h3 className="text-lg font-semibold mb-2 text-gray-900">
                Rate & Review
              </h3>
              <p className="text-gray-600">
                Share your honest thoughts with detailed 5-star ratings and 
                comprehensive reviews.
              </p>
            </div>

            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition hover:-translate-y-2">
              <BookOpen className="text-blue-600 mb-3" size={36} />
              <h3 className="text-lg font-semibold mb-2 text-gray-900">
                Discover Books
              </h3>
              <p className="text-gray-600">
                Browse thousands of books across multiple genres and find your 
                next great read.
              </p>
            </div>

            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition hover:-translate-y-2">
              <Heart className="text-red-500 mb-3" size={36} />
              <h3 className="text-lg font-semibold mb-2 text-gray-900">
                Community Driven
              </h3>
              <p className="text-gray-600">
                Connect with fellow book enthusiasts and get personalized 
                recommendations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-6 bg-indigo-600 text-white">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <Users size={40} className="mx-auto mb-3" />
              <div className="text-4xl font-bold mb-2">10K+</div>
              <p className="text-indigo-100">Active Readers</p>
            </div>

            <div>
              <BookOpen size={40} className="mx-auto mb-3" />
              <div className="text-4xl font-bold mb-2">50K+</div>
              <p className="text-indigo-100">Books Available</p>
            </div>

            <div>
              <TrendingUp size={40} className="mx-auto mb-3" />
              <div className="text-4xl font-bold mb-2">100K+</div>
              <p className="text-indigo-100">Reviews Published</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-6 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <Award className="text-indigo-600 mx-auto mb-4" size={40} />
          <h2 className="text-3xl font-bold mb-4 text-gray-900">
            Join Our Reading Community
          </h2>
          <p className="text-gray-600 mb-8 text-lg">
            Sign up today and become part of a vibrant community of book lovers 
            sharing their passion for reading.
          </p>
          <button
            onClick={onBooksClick}
            className="px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition"
          >
            Get Started Now
          </button>
        </div>
      </section>
    </div>
  );
}