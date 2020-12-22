let mongoUtil = require('../utils/mongoUtil');

const CitiesDAO = {}
/**
   * Finds and returns cities by country.
   * Returns a list of objects, each object contains a title and an _id.
   * @param {Object} filters - The search parameters to use in the query.
   * @param {number} page - The page of cities to retrieve.
   * @param {number} citiesPerPage - The number of cities to display per page.
   * @returns {GetcitiesResult} An object with movie results and total results
   * that would match this query
   */
CitiesDAO.getCities =  async function(sortType = null) {
  let cities = mongoUtil.getDb().collection('cities')
  let cursor
  try {
    console.log(sortType)
    cursor = await cities
      .find()
      .sort(sortType)
      .limit(20)
    const records = await cursor.toArray()
    return records
  } catch (e) {
    console.error(`Unable to issue find command, ${e}`)
    return []
  }
}

module.exports = CitiesDAO