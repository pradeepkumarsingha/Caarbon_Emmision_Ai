import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function Home() {
  return (
    <div className="relative bg-gray-900 text-white">
      {/* Hero section */}
      <div className="relative h-screen">
        <div className="absolute inset-0">
          <img
            src="/images/hero-windsurf.jpg"
            alt="Windsurfer riding waves at sunset"
            className="h-full w-full object-cover"
          />
          <div className="absolute inset-0 bg-black/60 mix-blend-multiply" />
        </div>
        <div className="relative mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 50 }} 
            animate={{ opacity: 1, y: 0 }} 
            transition={{ duration: 1 }}
            className="flex min-h-[70vh] flex-col justify-center text-center sm:text-left"
          >
            <h1 className="text-5xl font-extrabold tracking-tight sm:text-7xl">
            Less carbon, more future.,<br />Reduce carbon, revive nature.
            </h1>
            <p className="mt-6 max-w-xl text-lg text-gray-200">
              Experience the ultimate freedom of windsurfing. Join our community of passionate riders and discover the perfect blend of wind, water, and adventure.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row gap-6 justify-center sm:justify-start">
              <Link
                to="/equipment"
                className="rounded-lg bg-blue-500 px-6 py-3 text-lg font-semibold text-white shadow-md transition-all duration-300 hover:bg-blue-400 hover:scale-105"
              >
                Explore Equipment
              </Link>
              <Link
                to="/events"
                className="rounded-lg border border-white px-6 py-3 text-lg font-semibold text-white transition-all duration-300 hover:bg-white hover:text-gray-900 hover:scale-105"
              >
                View Events
              </Link>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Featured sections */}
      <div className="bg-gray-100 py-24 sm:py-32 text-gray-900">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-y-16 gap-x-12 lg:grid-cols-2">
            {/* Equipment Section */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }} 
              whileInView={{ opacity: 1, scale: 1 }} 
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="relative"
            >
              <img
                src="/images/equipment.jpg"
                alt="Windsurfing equipment"
                className="aspect-[3/2] w-full rounded-xl object-cover shadow-lg"
              />
              <div className="mt-8">
                <h2 className="text-4xl font-bold">Premium Equipment</h2>
                <p className="mt-4 text-lg text-gray-700">
                  Discover our curated selection of top-quality windsurfing gear for all skill levels.
                </p>
                <Link
                  to="/equipment"
                  className="mt-4 inline-block text-blue-600 font-semibold hover:text-blue-500 transition-colors"
                >
                  Browse Equipment →
                </Link>
              </div>
            </motion.div>

            {/* Events Section */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }} 
              whileInView={{ opacity: 1, scale: 1 }} 
              transition={{ duration: 0.8, delay: 0.2 }}
              viewport={{ once: true }}
              className="relative"
            >
              <img
                src="/images/events.jpg"
                alt="Windsurfing competition"
                className="aspect-[3/2] w-full rounded-xl object-cover shadow-lg"
              />
              <div className="mt-8">
                <h2 className="text-4xl font-bold">Upcoming Events</h2>
                <p className="mt-4 text-lg text-gray-700">
                  Join competitions, workshops, and community meetups around the world.
                </p>
                <Link
                  to="/events"
                  className="mt-4 inline-block text-blue-600 font-semibold hover:text-blue-500 transition-colors"
                >
                  View Calendar →
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
