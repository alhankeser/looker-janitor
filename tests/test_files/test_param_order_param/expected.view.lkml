view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  filter: a_filter_name {
    type: number
  }

  dimension: a_dimension_name {
    sql: ${TABLE}."a_dimension_name" ;;
    type: number
  }

  measure: a_measure_name {
    sql: ${TABLE}."a_dimension_name" ;;
    type: average
    filters: [
      something: "Yes",
    ]
  }
}
